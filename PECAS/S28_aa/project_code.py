# Code specific to this project. Copy this and rename it project_code.py, then fill in any function implementations
# you need, leaving the rest blank.

import aa_routines as pr
import os
import dump2csv as dc
_ps = pr._ps


# Called at the start of the run, after any resetting.
def before_run(ps=_ps):
    if ps.update_techopt:
        dc.dump_techopt(lambda: pr.connect_to_aa(ps), ps.scendir)
    if ps.update_inputs:
        dc.dump_pg_tbls(lambda: pr.connect_to_aa(ps), ps.scendir, ps.aa_schema, '^Inputs_')


# Called at the start of each model year, before any modules have run in that year.
def start_of_year(year,ps=_ps):
    dc.dump_pg_tbls(lambda: pr.connect_to_aa(ps),  ps.scendir, ps.aa_schema, '^'+str(year))
    syntar_f = '{}\\PopSynTargets.csv'.format(year)
    
    if not(os.path.exists(syntar_f)):
        cmd = 'copy /Y AllYears\\Working\\PopulationSynthesis\\PopSynTargets.csv {}\\PopSynTargets.csv'.format(year)
        print(cmd)
        os.system(cmd)
    skimyear = pr.get_skim_year(year, ps.skimyears)
    if skimyear<year:
        skimfilename = ps.skim_fname.format(yr=skimyear)
        if skimyear<ps.earliest_squeeze_year:
            dc.dump_pg_tbls(lambda: pr.connect_to_aa(ps), ps.scendir, ps.aa_schema, str(skimyear)+'_'+skimfilename[0:-4])
    
    if year==ps.baseyear:
        prev_year=year-1
        dc.dump_pg_tbls(lambda: pr.connect_to_aa(ps), ps.scendir, ps.aa_schema, '^'+str(prev_year))
    
    
def before_aa(year,ps=_ps):
    import sys, pandas
    os.chdir('..\\..\\Supply')
    sys.path.insert(0, '')
    from main import open_sites_file, open_mgra_io_file, run as supply_run
    
    # load dataframe(s)
    combined_rent = '..\\Demand\\{}\\combined_rents.csv'.format(year-1)
    old_supply_input = 'data\\forecasted_year_{}.csv'.format(year-1)
   
    if os.path.exists(combined_rent) and os.path.exists(old_supply_input) :
        from rents2supply import importRents
        mgra_dataframe = importRents(combined_rent,old_supply_input)
        #mgra_dataframe = pandas.read_csv(old_supply_input)
    elif os.path.exists(old_supply_input):
        mgra_dataframe = pandas.read_csv(old_supply_input)
    else:
        mgra_dataframe = open_mgra_io_file(from_database=True)
            
    planned_sites = open_sites_file(from_database=True)
    # start simulation
    supply_run(mgra_dataframe, planned_sites, year)
        
    cmd = 'copy /Y data\\output\\aa_export.csv ..\\PECAS\\S28_aa\\{}\\FloorspaceO.csv'.format(year)
    print(cmd)
    os.system(cmd)
    os.chdir('..\\PECAS\\S28_aa') 

# Called after the AA module finishes.
def after_aa(year, ps):
    import os
    act_location_file = '..\\PECAS\\S28_aa\\'+str(year)+'\\ActivityLocations.csv'
    os.chdir('..\\..\\Demand')
    if (os.path.exists(act_location_file)):
        cmd = 'rscript .\\R\\aa2demand.R ' + act_location_file + ' .. '+str(year-ps.baseyear)
    else:
        cmd = 'rscript .\\R\\aa2demand.R ..\\PECAS\\S28_aa\\2011\\ActivityLocations.csv  .. '+str(year-ps.baseyear)
    
    print(cmd)
    os.system(cmd)
    cmd = 'rscript .\\R\\evalDemand.R .. '+str(year) + ' '+ str(year)   
    print(cmd)
    os.system(cmd)
       
    os.chdir('..\\PECAS\\S28_aa') 


# Called after the ED module finishes.
    
def after_ed(year, ps=_ps):
    pass


# Called after the TM module finishes.
def after_tm(year, ps=_ps):
    pass


# Called after the SD module finishes.
def after_sd(year, ps=_ps):
    pass
