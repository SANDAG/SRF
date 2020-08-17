import csv
import importlib
import logging
import shutil
import subprocess
import sys
import threading
from os import path
from queue import Queue
import aa_routines as pr
import scriptutil as su

_ps = pr._ps

# These files are copied from the previous AA run in years where AA didn't run
output_file_list = [
    "ExchangeResults.csv",
    "TechnologyChoice.csv",
    "CommodityNumbers.csv",
    "ZonalMakeUse.csv",
    "ActivityLocations.csv",
    "ActivityLocations2.csv",
    "TAZDetailedUse.csv",
    "TAZDetailedMake.csv",
    "CommodityZUtilities.csv",
    "ExchangeResultsTotals.csv",
    "ActivityNumbers.csv",
    "Histograms.csv",
    "ActivitySummary.csv",
    "MakeUse.csv",
    "FloorspaceDelta.csv",
    "XVector.csv",
]


# noinspection PyMethodMayBeStatic
class StandardAARunner(pr.AARunner):
    def __init__(self):
        self.popsyn = StandardAARunner.PopSynRunner()

    def __del__(self):
        self.popsyn.stop()

    def run_aa(self, ps, year, skimfile, skimyear, dbyear=None, load=True):
        if dbyear is None:
            dbyear = year

        # Optional floorspace adjustments and import/export calculations
        if ps.floorspace_calc_delta:
            pr.write_floorspace_i(year, ps=ps)

        if ps.calculate_import_export_size:
            if year != ps.baseyear:
                pr.update_exporters(dbyear, ps=ps)
                pr.update_importers(dbyear, ps=ps)
                pr.write_activity_totals(year, dbyear, ps=ps)

        args, kwargs = self.make_aa_program_call(ps, year, skimyear, skimfile)

        retcode = subprocess.call(*args, **kwargs)
        pr.move_replace(ps.scendir + "/event.log", ps.scendir + "/" + str(year) + "/aa-event.log")
        # If this is a zero-iteration run, we're not expecting AA to converge, so don't crash when it doesn't!
        allowed_retcodes = [0, 2] if ps.aa_max_iterations == 0 else [0]
        pr.log_results_from_external_program(
            "AA model finished for year {}".format(year),
            "AA model did not run successfully in year {}".format(year),
            (retcode,),
            allowed_retcodes=allowed_retcodes
        )

        if year in ps.travel_model_input_years:
            #self.popsyn.register_tm_input("Popsyn")
            self.popsyn.push(StandardAARunner._Task("Popsyn", self.run_popsyn, ps, year))

        

    def make_aa_program_call(self, ps, year, skimyear, skimfile):
        """
        Returns the arguments that should be passed to subprocess.call to run the AA module, as a pair
        containing the positional arguments as a list and the keyword arguments as a dictionary.
        """

        classpath = pr.build_class_path_in_path(
            ps.codepath, ps.pecasjar, ps.commonbasejar,
            "or124.jar", "mtj.jar", "log4j-1.2.9.jar",
            "postgresql-8.4-701.jdbc4.jar", #"sqljdbc4.jar",
            ps.simpleormjar, "omx.jar", #"jarhdf5-2.10.0.jar",
            #"jarhdfobj.jar", "jarh5obj.jar",
            #"commons-math3-3.2.jar", "jarhdf-2.10.0.jar",
            #"netlib-java-0.9.3.jar", "arpack-combo-0.1.jar", "arpack_combined_all.jar"
        )

       

        logging.info("classpath is " + classpath)

        logging.info("Starting PECAS AA Model run for year " + str(year))
        # Run AA
        vm_args = [
            "-Xmx" + ps.aa_memory,
            "-cp", pr.build_class_path(ps.scendir + "AllYears/Inputs", classpath)
        ]

        self.add_properties(ps, vm_args, year, skimyear, skimfile)

        if ps.profiling:
            vm_args.append("-Xrunhprof:cpu=samples,file=hprof.txt,depth=24,thread=y")
        if False and ps.missionControl:
            vm_args.append("-XX:+UnlockCommercialFeatures")
            vm_args.append("-XX:+FlightRecorder")
            vm_args.append("-XX:+UnlockDiagnosticVMOptions")
            vm_args.append("-XX:+DebugNonSafepoints")

        logging.info("Running AA with " + " ".join(vm_args))

        return [
            [ps.javaRunCommand] +
            vm_args +
            ["com.hbaspecto.pecas.aa.control.AAControl"]
        ], {}

    def add_properties(self, ps, vm_args, year, skimyear, skimfile):
        if year in ps.constrainedyears:
            constrained = True
        else:
            constrained = False

        prevyear = year - 1
        logging.debug("prevyear =" + str(prevyear))

        properties = dict(
            {
                "log4j.configuration": "log4j.xml",
                "java.library.path": pr.get_native_path(),
            },
            SCENDIR=ps.scendir,
            YEAR=year,
            SKIMYEAR=skimyear,
            SKIMFILE=skimfile,
            PREVYEAR=prevyear,
            CONSTRAINED=constrained,
            GROUPBOUNDS=ps.aa_group_bounds,
            MAXITS=ps.aa_max_iterations,
            INITSTEP=ps.aa_initial_step_size,
            MINSTEP=ps.aa_minimum_step_size,
            MAXSTEP=ps.aa_maximum_step_size,
            FSZONES=ps.use_floorspace_zones,
            MAXTOTAL=ps.max_total_clearance,
            MAXSPEC=ps.max_specific_clearance,
            AZVI=ps.use_activities_zonal_values_i,
            CONSTSIZE=ps.update_construction_size_terms,
            XVECTORCONSTANTS=year > ps.baseyear and ps.xvector_constants,
            TRIPMAT=(year in ps.travel_model_input_years)  and ps.make_trip_matrices,
            POISSON=ps.poisson_trips,
            EMMETRIPS=ps.emme_format_trips,
            SECONDRUN=(not (constrained and ps.aa_max_iterations == 0)),
            STOPMISMATCH=ps.stop_on_constraint_mismatch,
            MAXTHREADS=getattr(ps, 'aa_maxthreads', 12)
        )

        vm_args.extend(pr.vm_properties(properties))

    def run_popsyn(self, ps, year):
        logging.info("Running the population synthesizer for year {}".format(year))
        # noinspection PyBroadException
        try:
            _run_popsyn(ps, year)
        except Exception as e:
            logging.error("Population synthesizer failed: {}".format(e))

    class PopSynRunner(threading.Thread):

        def __init__(self):
            super().__init__()
            self.q = Queue()
            self._stop_ = threading.Event()


        def push(self, task):
            self.q.put(task)

        def stop(self):
            self._stop_.set()

        def run(self):
            # noinspection PyBroadException
            try:
                while True:
                    if self._stop_.is_set():
                        break

                    if not self.q.empty():
                        task = self.q.get()
                        if task is None:
                            break
                        else:
                            task.run()

            except Exception as e:
                logging.error("Population synthesis thread failed: {}".format(e))

 

    class _Task:
        def __init__(self, name, method, ps, year):
            self.name = name
            self.method = method
            self.year = year
            self.ps = ps

        def run(self):
            self.method(self.ps, self.year)


def _run_popsyn(ps, year):
    scendir = path.abspath(ps.scendir)
    targets_fname = "PopSynTargets.csv"
    targets_fpath = path.join(scendir, str(year), targets_fname)
    _scale_popsyn_targets(ps, targets_fpath)
    popsyndir = path.abspath(ps.popsyndir)
    shutil.copy(targets_fpath, path.join(popsyndir, targets_fname))
    
    prev_fname = "Output"+ps.popsyn_samples_file
    
    seed_fname = "Seed"+ps.popsyn_samples_file
    seed_path = path.join(scendir, str(year), seed_fname)
    if not path.exists(seed_path):
        seed_path = path.join(scendir, "AllYears", "Inputs", seed_fname)
        if not path.exists(seed_path):
            seed_path = None
    if seed_path:
        shutil.copy(seed_path, path.join(popsyndir, prev_fname))

    classpath = pr.build_class_path_in_path(
        path.abspath(ps.codepath),
        ps.popsynjar, "log4j-1.2.9.jar", "commons-math3-3.2.jar"
    )
    vm_args = [
        "-Xmx" + ps.pop_syn_memory,
        "-cp", pr.build_class_path(
            path.join(scendir, "AllYears/Inputs"),
            popsyndir,
            classpath
        )
    ]

    logging.info("Running pop synth for {} with {}".format(year, " ".join(vm_args)))
    retcode = subprocess.call(
        [ps.javaRunCommand] +
        vm_args +
        ["com.hbaspecto.synthesizer.GeneratePopulation", "Synth.properties"],
        cwd=popsyndir
    )
    pr.log_results_from_external_program(
        "Pop synth finished for year {}".format(year),
        "Pop synth did not run successfully in year {}".format(year),
        (retcode,)
    )

    shutil.copy(path.join(popsyndir, prev_fname), path.join(scendir, str(year), prev_fname))


def _scale_popsyn_targets(ps, fpath):
    try:
        scale_path = path.join(ps.scendir, "AllYears", "Inputs", "PopSynEmploymentScaleFactors.csv")

        with open(scale_path, 'r') as scale_f:
            reader = csv.reader(scale_f)
            next(reader)
            scale_factors = {k: float(v) for k, v in reader}

        su.backup(fpath, "_unscaled")

        with open(fpath, 'r') as target_f:
            reader = csv.reader(target_f)
            target_header = next(reader)
            target_rows = list(reader)

        taz_col = target_header.index("TAZ")
        emp_cols = [(i, col.split("_")[2]) for (i, col) in enumerate(target_header) if col.startswith("empin_occ")]

        for row in target_rows:
            if int(row[taz_col]) == 0:
                continue
            test_emp = row[emp_cols[0][0]]
            if test_emp == "" or float(test_emp) < 0:
                continue

            for col, code in emp_cols:
                scale_code = "NC" + code
                scale_factor = scale_factors[scale_code]
                row[col] = str(float(row[col]) * scale_factor)

        with open(fpath, 'w', newline="") as target_f:
            writer = csv.writer(target_f)
            writer.writerow(target_header)
            for row in target_rows:
                writer.writerow(row)
    except IOError:
        logging.info("PopSynEmploymentScaleFactors file not found, skipping this step")

def get_args_and_run():
    pr.set_up_logging()
    args = sys.argv + ["", ""]
    print("Args are" + str(args))
    _year = int(args[1])

    if args[2] and args[2] != "--rerun":
        main_ps_name = args[2]
        main_ps = importlib.import_module(main_ps_name)
    else:
        import aa_settings as main_ps

    have_org = False
    if args[2] == "--rerun" or args[3] == "--rerun":
        logging.info("Rerunning AA in " + str(_year) + " with solved prices from ExchangeResults.csv")
        have_org = True
        try:
            shutil.move(main_ps.scendir + "/" + str(_year) + "/ExchangeResultsI.csv",
                        main_ps.scendir + "/" + str(_year) + "/ExchangeResultsI-orig.csv")
        except FileNotFoundError:
            have_org = False
        shutil.copyfile(main_ps.scendir + "/" + str(_year) + "/ExchangeResults.csv",
                        main_ps.scendir + "/" + str(_year) + "/ExchangeResultsI.csv")

    _skimyear = pr.get_skim_year(_year, main_ps.skimyears)
    skimfilename = main_ps.skim_fname.format(yr=_skimyear)

    aa = StandardAARunner()
    aa.popsyn.start()

    try:
        logging.info("Running aa in year " + str(_year))
        # noinspection PyTypeChecker
        aa.run_aa(main_ps, _year, skimfilename, _skimyear, dbyear=None, load=False)

        if have_org:
            shutil.move(main_ps.scendir + "/" + str(_year) + "/ExchangeResultsI-orig.csv",
                        main_ps.scendir + "/" + str(_year) + "/ExchangeResultsI.csv")
    finally:
        aa.popsyn.stop()


if __name__ == "__main__":
    get_args_and_run()
