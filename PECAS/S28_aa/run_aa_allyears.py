import importlib
import logging
import shutil
import sys
import threading
from os.path import join, exists
from queue import Queue
from typing import List
import aa_routines as pr
#import phasing as ph
import project_code
#import reset_database as rd
import run_aa as aa
#import sd_backup_restore as sbr
import skims_to_sem as skims
#import update_techopt as uto

_ps = pr._ps



# noinspection PyBroadException,PyUnboundLocalVariable
def main(ps, aa_runner=aa.StandardAARunner()):
    try:
        ps.travel_model_input_years = sorted(set(ps.travel_model_input_years))
  
        main_impl(ps, aa_runner)
    except Exception as e:
        import traceback
        logging.fatal(repr(e))
        for line in traceback.format_tb(e.__traceback__):
            logging.fatal(line)
        
        aa_runner.popsyn.stop()
        raise e

# noinspection PyUnusedLocal
def pre_check(ps, aa_runner,year):
    """
    Does "pre-flight" checks - checks for common setup problems
    that might cause a crash hours or days later but can be identified now.
    """

    # Check that all year directories exist
    if year in pr.irange(ps.baseyear, ps.stopyear):
        if not exists(join(ps.scendir, str(year))):
            raise PrecheckFailure(f"There is no year directory for the run year {year}")

    # Check that the PopSynBaseTargets file exists in all years where the population synthesizer will run
    if year in ps.travel_model_input_years:
        if not exists(join(ps.scendir, str(year), "PopSynBaseTargets.csv")):
            raise PrecheckFailure(f"There is no PopSynBaseTargets file for year {year}")


class PrecheckFailure(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def read_resume():
    with open("resume.txt", "r") as resume_file:
        resume_code = next(resume_file).strip()
        year = int(resume_code)
        return year


def write_resume(ps, resume_year):
    try:
        with open(join(ps.scendir, "resume.txt"), "w") as resume_file:
            resume_file.write(str(resume_year))

    except IOError:
        pass
    
# noinspection PyBroadException
def main_impl(ps, aa_runner):
    logging.info("Recreate the inputs and yearly folder structure by downloading data from pg")
    import os
    #cmd = 'python dump2csv.py'
    #os.system(cmd) 

    logging.info("**********************")
    logging.info(
        "Starting PECAS Run in " + ps.scendir +
        ". scenario " + ps.scenario +
        ", AA schema " + ps.aa_schema)

    if ps.travel_model_input_years:
        aa_runner.popsyn.start()   


    if ps.resume_run:
        try:
            year = read_resume()           
        except (IOError, ValueError):
            logging.warning(
                "No valid resume file; exiting; you can set resume_run to false if you want to start over")
            raise
    else:
        year = ps.baseyear
        

    converted_skims = set()


    project_code.before_run(ps=ps)
    
    

    # ------------------------------------------------------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------------------------------------------------------

    while year <= ps.stopyear:
        write_resume(ps, year)  
        
        skimyear = pr.get_skim_year(year, ps.skimyears)
        skimfilename = ps.skim_fname.format(yr=skimyear)

        project_code.start_of_year(year, ps=ps)
        
        pre_check(ps, aa_runner, year)
        if year>2012:
            project_code.before_aa(year, ps=ps)
        
        # --------------------------------------------------------------------------------------------------------------
        # AA module
        # --------------------------------------------------------------------------------------------------------------

        if year >= ps.aa_startyear:
           
            if ps.squeeze_skims and skimyear >= ps.earliest_squeeze_year and skimyear not in converted_skims:
                 #skims.main(skimyear, ps)
                 cmd = 'python skims_to_sem.py '+str(skimyear)
                 os.system(cmd)   
                 converted_skims.add(skimyear)
                
            if year in ps.aayears:
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

        project_code.after_aa(year, ps=ps)
        year = year + 1
    
    if ps.travel_model_input_years:
        aa_runner.popsyn.push(None)
        logging.info("Waiting for the employment/population synthesizer thread")
        aa_runner.popsyn.join()
        logging.info("Employment/population synthesizer thread finished")


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
    else:
        ps_name = "aa_settings"

    main_ps = importlib.import_module(ps_name)

    if resume:
        main_ps.resume_run = True

    logging.info("Running with settings module {!r}".format(ps_name))
    # noinspection PyTypeChecker
    main(main_ps)
    logging.info("Done!")
