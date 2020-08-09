# Code specific to this project. Copy this and rename it project_code.py, then fill in any function implementations
# you need, leaving the rest blank.

import aa_routines as pr
import dump2csv as dc
_ps = pr._ps


# Called at the start of the run, after any resetting.
def before_run(ps=_ps):
    pass
 

# Called at the start of each model year, before any modules have run in that year.
def start_of_year(year,ps=_ps):
    pass 
    


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
