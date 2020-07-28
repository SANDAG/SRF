import importlib
import logging
import shutil
import sys
import threading
from os.path import join, exists
from queue import Queue
from typing import List

import pecas_routines as pr
import phasing as ph
import project_code
import reset_database as rd
import run_aa as aa
import run_ed as ed
import run_sd as sd
import sd_backup_restore as sbr
import skims_to_sem as skims
import update_techopt as uto

_ps = pr._ps


class MapitLazyLoader(threading.Thread):
    instances = []

    q = None
    ps = None
    load = None
    name = "MapIt Lazy Loader"

    def __init__(self, q, load=None, ps=_ps):
        logging.info("Starting MapIt Lazy Loader consumer thread")

        super(MapitLazyLoader, self).__init__()
        self.q = q
        self.load = load or pr.load_outputs_for_year
        self.ps = ps

        self._stop_ = threading.Event()

        MapitLazyLoader.instances.append(self)

    def stop(self):
        logging.info("Halting MapIt Lazy Loader consumer thread")
        self._stop_.set()
        self.unregister()

    @property
    def stopped(self):
        return self._stop_.is_set()

    def unregister(self):
        try:
            i = MapitLazyLoader.instances.index(self)
            del MapitLazyLoader.instances[i]
        except ValueError:
            pass

    def __del__(self):
        self.unregister()

    def run(self):
        while True:
            if self.stopped:
                # Abort! Abort!
                break

            if not self.q.empty():
                job = self.q.get()
                if job is None:
                    # Flag to indicate PECAS is done generating data
                    break

                logging.info("Lazily loading sequence {0[sequence]} in {0[year]} to MapIt".format(job))
                self.load(**job, ps=self.ps)


# noinspection PyBroadException,PyUnboundLocalVariable
def main(ps, aa_runner=aa.StandardAARunner(), sd_runner=sd.StandardSDRunner(), tm_runner=None):
    try:
        if ps.use_tm and tm_runner is None:
            import run_tm as tm
            tm_runner = tm.TMRunner()
        ps.travel_model_input_years = sorted(set(ps.travel_model_input_years) | set(ps.tmyears))
        pre_check(ps, aa_runner, sd_runner, tm_runner)
        main_impl(ps, aa_runner, sd_runner, tm_runner)
    except Exception as e:
        import traceback
        logging.fatal(repr(e))
        for line in traceback.format_tb(e.__traceback__):
            logging.fatal(line)
        for t in MapitLazyLoader.instances:
            t.stop()
            del t
        aa_runner.popsyn.stop()
        raise e


# noinspection PyUnusedLocal
def pre_check(ps, aa_runner, sd_runner, tm_runner):
    """
    Does "pre-flight" checks - checks for common setup problems
    that might cause a crash hours or days later but can be identified now.
    """

    # Check that all year directories exist
    for year in pr.irange(ps.baseyear, ps.stopyear):
        if not exists(join(ps.scendir, str(year))):
            raise PrecheckFailure(f"There is no year directory for the run year {year}")

    # Check that the PopSynBaseTargets file exists in all years where the population synthesizer will run
    for year in ps.travel_model_input_years:
        if not exists(join(ps.scendir, str(year), "PopSynBaseTargets.csv")):
            raise PrecheckFailure(f"There is no PopSynBaseTargets file for year {year}")

    # Check that the travel model is available and set up consistently
    if ps.use_tm:
        if not tm_runner.tm_is_available():
            raise PrecheckFailure("The travel model is busy; check for lock files")
        precheck_error = tm_runner.tm_precheck(ps)
        if precheck_error:
            raise PrecheckFailure(precheck_error)


class PrecheckFailure(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# noinspection PyBroadException
def main_impl(ps, aa_runner, sd_runner, tm_runner):
    cityphi = None
    if ps.generate_cityphi:
        import cityphi

    logging.info("**********************")
    logging.info(
        "Starting PECAS Run in " + ps.scendir +
        ". MapIt scenario " + ps.scenario +
        ", SD schema " + ps.sd_schema)

    mq = None
    mll = None
    if ps.load_output_to_mapit:
        mq = Queue()  # conveniently thread-safe
        mll = MapitLazyLoader(q=mq, ps=ps)
        mll.start()
    if ps.travel_model_input_years or ps.employment:
        aa_runner.popsyn.start()

    if ps.resume_run:
        try:
            year, skip_sd = read_resume()
            if ps.load_output_to_mapit:
                pr.clear_upload(year, ps=ps)
        except (IOError, ValueError):
            logging.warning(
                "No valid resume file; exiting; you can set resume_run to false if you want to start over")
            raise
    else:
        year = ps.baseyear
        skip_sd = False
        if ps.reset_initial_database:
            reset_database(ps.aa_startyear, ps=ps)
        if ps.generate_cityphi:
            try:
                cityphi.recreate_crosstab(ps=ps)
            except Exception:
                # ignore - If SD didn't run at all, there will be no outputs anyway.
                pass
        if ps.load_output_to_mapit:
            rd.clear_mapit_outputs(ps=ps)

        if ps.adaptive_phasing:
            ph.clear_manual_zoning_in_phasing_plans(ps=ps)
            ph.set_plan_phase_dict(ps=ps)
            ph.update_parcel_zoning_xref_according_to_adaptive_phasing(year, ps=ps)

        if ps.scenario_ed_base is not None:
            ed.begin_all_acttot(ps=ps)

    converted_skims = set()

    if ps.use_tm:
        aa_runner.popsyn.init_tm_input_years(ps.travel_model_input_years)

    run_ed = (ps.scenario_ed_inputs is not None) or ps.ed_from_files

    project_code.before_run(ps=ps)

    # ------------------------------------------------------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------------------------------------------------------

    while year <= ps.stopyear:
        write_resume(ps, year)

        skimyear = pr.get_skim_year(year, ps.skimyears)
        skimfilename = ps.skim_fname.format(yr=skimyear)

        project_code.start_of_year(year, ps=ps)

        # --------------------------------------------------------------------------------------------------------------
        # AA module
        # --------------------------------------------------------------------------------------------------------------

        if year >= ps.aa_startyear:
            if ps.use_tm and skimyear >= ps.earliest_squeeze_year and skimyear not in converted_skims:
                tm_runner.retrieve_skims(ps, skimyear)
                if ps.squeeze_skims:
                    skims.main(skimyear, ps)
                converted_skims.add(skimyear)
            elif ps.squeeze_skims and skimyear >= ps.earliest_squeeze_year and skimyear not in converted_skims:
                skims.main(skimyear, ps)
                converted_skims.add(skimyear)

            if year in ps.aayears:
                if ps.scenario_base is not None:
                    aa.import_exchange_results(ps, ps.scenario_base, year)
                    aa.import_constants(ps, ps.scenario_base, year)
                aa_runner.run_aa(ps, year, str(skimfilename), skimyear)
            else:
                if year == ps.baseyear:
                    logging.error("You need to run AA in the base year, check aayears!")
                    raise ValueError
                else:
                    # need to copy all of the stuff from last year
                    for file in aa.output_file_list:
                        try:
                            shutil.copyfile(ps.scendir + "/" + str(year - 1) + "/" + file,
                                            ps.scendir + "/" + str(year) + "/" + file)
                        except IOError:
                            logging.warning(
                                "Couldn't copy " + str(file) + " from year " + str(year - 1) + " to year " + str(year))
                    if ps.load_output_to_mapit:
                        pr.load_outputs_for_year(ps, year, ps.EAGER_AA)
        elif ps.load_output_to_mapit:
            # Normally the runAA command loads its output to mapit, but if AA didn't run we need to do it here
            pr.load_outputs_for_year(ps, year, ps.EAGER_AA)

        if ps.scale_technology_options and not run_ed and year == ps.baseyear:
            uto.create_all_acttot_techopt(lambda: pr.connect_to_sd(ps=ps), ".", ps=ps)

        if ps.load_output_to_mapit:
            mq.put({
                'year': year,
                'sequence': ps.LAZY_AA
            })

        if ps.use_aa_to_sd_price_ratio and year == ps.baseyear:
            pr.calculate_aa_to_sd_price_correction(ps=ps)

        project_code.after_aa(year, ps=ps)

        # Atlanta Specific
        if ps.allocate_am_totals:
            pr.write_abm_land_use(year, ps=ps)
        if ps.labour_make_use:
            pr.write_labor_make_use(year, ps=ps)

        # --------------------------------------------------------------------------------------------------------------
        # ED module
        # --------------------------------------------------------------------------------------------------------------

        if ps.scenario_ed_base is not None and not run_ed and year > ps.baseyear:
            ed.update_activity_totals(year, ps=ps)

        if run_ed and year == ps.baseyear:
            if ps.scenario_ed_inputs is not None:
                ed.dump_updated_activity_totals(
                    lambda: pr.connect_to_mapit(ps=ps),
                    ps=ps)

            uto.create_all_acttot_techopt(
                lambda: pr.connect_to_sd(ps=ps), ".",
                acttot_src=ed.activity_totals_ed_input_path(ps=ps),
                ps=ps
            )

        project_code.after_ed(year, ps=ps)

        # --------------------------------------------------------------------------------------------------------------
        # TM module
        # --------------------------------------------------------------------------------------------------------------

        do_tm = (
            ps.use_tm and
            year in ps.tmyears and
            year >= ps.tm_startyear
        )
        if do_tm:
            logging.info("Starting PECAS TM Model run for year {}".format(year))
            aa_runner.popsyn.wait_for_tm_inputs(year)
            tm_runner.run_tm(ps, year)
            logging.info("TM model finished for year {}".format(year))

        project_code.after_tm(year, ps=ps)

        # --------------------------------------------------------------------------------------------------------------
        # SD module
        # --------------------------------------------------------------------------------------------------------------

        if ps.use_sd and year < ps.stopyear:  # SD is not run or replayed in the last year
            if skip_sd:
                skip_sd = False
            elif year >= ps.sd_startyear:
                if ps.use_aa_to_sd_price_ratio:
                    pr.apply_aa_to_sd_price_correction(year, ps=ps)
                if year in ps.find_expected_values_years:
                    find_expected_values(year, ps=ps)
                sd_runner.run_sd(ps, year, str(skimfilename), skimyear)
            else:
                pr.replay_development_events_for_year(year, ps=ps)

                if ps.load_output_to_mapit:
                    pr.load_outputs_for_year(ps, year, ps.EAGER_SD)

            write_resume(ps, year, skip_sd=True)

            if ps.load_output_to_mapit:
                mq.put({
                    'year': year,
                    'sequence': ps.LAZY_SD
                })

            if ps.use_aa_to_sd_price_ratio and year >= ps.sd_startyear:
                # TODO SD should use SDPrices.csv if it exists, instead of reading ExchangeResults.csv.
                shutil.copyfile(ps.scendir + "/" + str(year) + "/AAExchangeResults.csv",
                                ps.scendir + "/" + str(year) + "/ExchangeResults.csv")
            if (year + 1) in ps.snapshotyears:
                pr.snapshot_parcels(year + 1, ps=ps)
                if ps.generate_cityphi:
                    cityphi.add_year_to_crosstab(year + 1, ps=ps)

            if ps.adaptive_phasing:
                ph.update_parcel_zoning_xref_according_to_adaptive_phasing(year + 1, ps=ps)

        write_floorspace_summary = (
            ps.use_sd and
            ps.sd_startyear > year >= ps.aa_startyear - 1 and
            year < ps.endyear
        )
        if write_floorspace_summary:
            # AA is going to run next year, but SD didn't run. Prepare
            # FloorspaceO and FloorspaceSD.
            pr.write_floorspace_summary_from_parcel_file(str(year + 1), ps=ps)
            pr.copy_floorspace_summary(year + 1, ps=ps)

        if ps.labour_make_use:
            pr.write_labor_make_use(year, ps=ps)

        project_code.after_sd(year, ps=ps)

        year = year + 1

    if ps.load_output_to_mapit:
        mq.put(None)
        logging.info("Done running PECAS. Waiting for MapIt lazy loader to finish.")
        mll.join()
        logging.info("Lazy loader finished.")

    if ps.travel_model_input_years or ps.employment:
        aa_runner.popsyn.push(None)
        logging.info("Waiting for the employment/population synthesizer thread")
        aa_runner.popsyn.join()
        logging.info("Employment/population synthesizer thread finished")


def read_resume():
    with open("resume.txt", "r") as resume_file:
        resume_code = next(resume_file).strip()
        skip_sd = False
        if resume_code.endswith("nosd"):
            skip_sd = True
            resume_code = resume_code[:-4]
        year = int(resume_code)
        return year, skip_sd


def write_resume(ps, resume_year, skip_sd=False):
    try:
        with open(join(ps.scendir, "resume.txt"), "w") as resume_file:
            resume_file.write(str(resume_year))
            if skip_sd:
                resume_file.write("nosd")
    except IOError:
        pass


def reset_database(aa_startyear, ps=_ps):
    sbr.restore_sd(ps, combine=True, schema=ps.sd_schema, threaded=False)
    if aa_startyear <= ps.baseyear:
        # Write out the base year FloorspaceI to ensure that the new run is
        # consistent with the database.
        # But DON'T DO THIS if we aren't running AA in the base year!
        pr.write_floorspace_summary_from_parcel_file(ps.baseyear, ps=ps)
        pr.copy_floorspace_summary(ps.baseyear, ps=ps)


def find_expected_values(year, ps=_ps):
    def ip(fname):
        return join(ps.inputpath, fname)

    shutil.copyfile(ip("sd.properties"), ip("sd_backup.properties"))

    try:
        pr.move_replace(ip("sd_calib.properties"), ip("sd.properties"))
        shutil.copyfile(ip("sd.properties"), ip("sd_calib.properties"))

        import propedit
        props = propedit.load_props(ip("sd.properties"))
        props.set_prop("CapacityConstrained", False)
        props.set_prop("LimitSpaceByTAZ", False)
        props.set_prop("sdorm.parcels", ps.expected_value_parcels)
        props.set_prop("EstimationTargetFile", ps.expected_value_targets)
        props.set_prop("EstimationMaxIterations", 0)
        props.new_prop("EstimationExpectedValuesOnly", True)
        props.save_props(ip("sd.properties"))

        pr.move_replace(ip("sd.properties"), ip("sd_ev_edited.properties"))
        shutil.copyfile(ip("sd_ev_edited.properties"), ip("sd.properties"))

        import sdcalib
        sdcalib.main(year, ps=ps)
        pr.move_replace(
            join(ps.scendir, "event.log"), join(ps.scendir, str(year), "ev_event.log"))
        pr.move_replace(
            join(ps.scendir, "expected_values.csv"), join(ps.scendir, str(year), "expected_values.csv"))
    finally:
        pr.move_replace(ip("sd_backup.properties"), ip("sd.properties"))


def _pull(seq: List[str], item: str) -> bool:
    if item in seq:
        seq.remove(item)
        return True
    else:
        return False


if __name__ == "__main__":
    pr.set_up_logging()
    args = [arg.lower() for arg in sys.argv]
    resume = _pull(args, "resume")
    if len(args) > 1:
        ps_name = args[-1]
        main_ps = importlib.import_module(ps_name)
    else:
        ps_name = "pecas_settings"
        # noinspection PyUnresolvedReferences
        import pecas_settings as main_ps

    if resume:
        main_ps.resume_run = True

    logging.info("Running with settings module {!r}".format(ps_name))
    # noinspection PyTypeChecker
    main(main_ps)
    logging.info("Done!")
