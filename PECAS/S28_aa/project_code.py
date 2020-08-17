# Code specific to this project. Copy this and rename it project_code.py, then fill in any function implementations
# you need, leaving the rest blank.

import aa_routines as pr
import dump2csv as dc
_ps = pr._ps


# Called at the start of the run, after any resetting.
def before_run(ps=_ps):
    
    dc.dump_techopt(lambda: pr.connect_to_aa(ps), ps.scendir)
    dc.dump_pg_tbls(lambda: pr.connect_to_aa(ps), ps.scendir, ps.aa_schema, '^Inputs_')


# Called at the start of each model year, before any modules have run in that year.
def start_of_year(year,ps=_ps):
    dc.dump_pg_tbls(lambda: pr.connect_to_aa(ps),  ps.scendir, ps.aa_schema, str(year))
    skimyear = pr.get_skim_year(year, ps.skimyears)
    skimfilename = ps.skim_fname.format(yr=skimyear)
    if skimyear<ps.earliest_squeeze_year:
        dc.dump_pg_tbls(lambda: pr.connect_to_aa(ps), ps.scendir, ps.aa_schema, str(skimyear)+'_'+skimfilename[0:-4])
    
    if year==ps.baseyear:
        prev_year=year-1
        dc.dump_pg_tbls(lambda: pr.connect_to_aa(ps), ps.scendir, ps.aa_schema, str(prev_year))
    
    


# Called after the AA module finishes.
def after_aa(year, ps=_ps):
    pass


# Called after the ED module finishes.
def after_ed(year, ps=_ps):
    pass


# Called after the TM module finishes.
def after_tm(year, ps=_ps):
    pass


# Called after the SD module finishes.
def after_sd(year, ps=_ps):
    pass
