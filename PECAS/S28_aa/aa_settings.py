# Scenario-specific settings for PECAS.
# To update a scenario's pecas_settings.py to the latest format:
#   1. Copy this file into the scenario's root folder, overwriting the existing file.
#   2. Open a terminal window (cmd, Powershell, bash, etc.) in the scenario's root folder.
#   3. Run the command "python update_settings.py"
#       (replacing "python" with the value of the pythonCommand setting in machine_settings.py)
#   4. Fill in values for any new settings that have been introduced.

# ----------------------------------------------------------------------------------------------------------------------
# INITIALIZATION
# ----------------------------------------------------------------------------------------------------------------------

# Re-export all machine-specific settings so they can be referenced through this module.
import sys
sys.path.append("../..")
from machine_settings import *
#from mapit_settings import *

from scriptutil import irange
from os.path import join

# ----------------------------------------------------------------------------------------------------------------------
# SETTINGS START HERE
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# FREQUENTLY CHANGED SETTINGS
# These MUST be checked for correctness before EVERY RUN.
# ----------------------------------------------------------------------------------------------------------------------
# # PECAS run configuration
scendir = "./"  # "./" means current directory, i.e. usually the same directory where this file is located

#input database setting
sd_schema = 'squeeze_skim'   #skim_2_pem intermediate results and output will be stored h

aa_schema = 's28'

# The name of the scenario, used by MapIt to identify outputs from this scenario.
# This starts with an UPPERCASE letter, e.g. "W25" or "S14b".
scenario = "S28"

# The base scenario that this scenario will get its starting prices and AA constants from; None if no base scenario
scenario_base = None # Enter a base scenario name e.g. "I174"

# Whether or not to resume the model from where it has stopped or crashed.
# This should normally be set to False.
# If this is set to True, the model will retry starting from the beginning of the year that was in
# progress when the run was interrupted.
# Resuming can also be enabled FOR ONE RUN ONLY as a command-line argument, e.g.
# "python runpecas.py resume". Use the command-line argument if possible.
# This was designed to be used in case a run crashes due to hardware problems such as a power failure.
# In any other case, instead using this resume feature, consider replaying by changing aa_startyear and sd_startyear below
# WARNING If this is set to True you probably need to change it back to False
resume_run = False
#resume_run=True

# --- REPLAY FUNCTIONALITY ---
# The first year in which AA is run.
# If this is equal to baseyear, AA will run normally.
# If it is later than the base year, existing AA results are used for all years before aa_startyear.
# You can only use existing AA results if you are re-running the scenario on the same machine,
# as AA results are not pre-populated when setting up a scenario to run.
# This is frequently used when the inputs for a future year have been updated. For instance,
# if new skims from the travel model are provided for year 2029, you could set the start year to 2030 and
# rerun your scenario. 
aa_startyear = 2012

# --- END OF REPLAY FUNCTIONALITY ---

# The last year in which AA is run. SD stops one year before this. 
# You can use this to stop the run early, to save electricity costs while you
# are waiting to update some input files on a future year.  
# You do not need to use this to stop the run early.  Instead, you can stop it interactively with
# MrsGui once it has progressed past the point where you want to update some inputs
stopyear = 2025

# Whether to scale the total amounts of activity (ActivityTotalsI) and the technology vectors
# (TechnologyOptionsI) as the model runs through time, in response to the model results.
# This should normally be set to True.
# It should only be set to False if this project is not using technology scaling, or as a time-
# saving option when REPLAYING a run that has already done technology scaling.
scale_technology_options = False

# The earliest skim year in which skims need to be squeezed.
# Set this to the base year if all skims need to be squeezed.
# Set this to a later year if the squeezed skims for previous years are already included in the
# scenario (e.g. because the scenario has already been run up to that point),
# to prevent the model from re-squeezing them.
#earliest_squeeze_year = 9999
earliest_squeeze_year = 2012

# XVectorConstants are used to adjust the AA constants over time based on changing values
# in XVector.csv in each year.  The constrained constants from the base year are
# reinterpreted by subtracting out the base year XVector effects, and then in future
# years the updated XVector effects are added back in.
# You need code in project_code.py to generate the file XVector.csv before you can  
# use the XVector functionality.
xvector_constants = False

# Other checks
# - machine_settings.py must be present in the scenario root folder.
# - Skims must be present in every skim year.

# ----------------------------------------------------------------------------------------------------------------------
# RUN YEARS
# ----------------------------------------------------------------------------------------------------------------------

# Simulation base year; usually shouldn't change for a given project.
baseyear = 2012

# Simulation end year; usually shouldn't change for a given project.
endyear = 2050

# Years in which new skims are available
skimyears = [2012,2016]

# Years in which AA should run
aayears = irange(baseyear, endyear)

# Years in which AA should run constrained
constrainedyears = [2012]

# Years in which the travel model should run
#tmyears = []

# ----------------------------------------------------------------------------------------------------------------------
# RUN DIRECTORY SETTINGS
# ----------------------------------------------------------------------------------------------------------------------

# Path where the PECAS jar files can be found
codepath = join(scendir,"AllYears","Code")
# Path where the PECAS general input files can be found
inputpath = join(scendir, "AllYears", "Inputs")
# Path where the PECAS general output files are written
outputpath = join(scendir, "AllYears", "Outputs")
# Path where population synthesis occurs
popsyndir = join(scendir, "AllYears", "Working", "PopulationSynthesis")

# ----------------------------------------------------------------------------------------------------------------------
# OUTPUT SETTINGS
# ----------------------------------------------------------------------------------------------------------------------

# Whether to load outputs to the MapIt database for showing result maps
# True or False - can also specify "http" or "sql" (instead of True) to force using a particular loader
#load_output_to_mapit = False
# Whether to generate outputs for CityPhi visualization
#generate_cityphi = False
# Whether to generate labour make/use summaries
#labour_make_use = False

# ----------------------------------------------------------------------------------------------------------------------
# AA CONFIGURATION
# ----------------------------------------------------------------------------------------------------------------------

# The maximum number of iterations to run in AA; usually several hundred at least, but may be set to zero for certain
# applications to see the distribution of activities at predetermined prices.
aa_max_iterations = 1500
# Initial step size in AA. Increasing this makes AA begin with more aggressive steps, so it wastes less time at the
# beginning but has a greater risk of overflowing.
aa_initial_step_size = 0.01
# Minimum step size in AA. Increasing this makes AA quicker to search elsewhere if it can't make progress.
aa_minimum_step_size = 0.002
# Maximum step size in AA. Increasing this makes AA more aggressive when it is making progress, but increases the risk
# of overflow.
aa_maximum_step_size = 1.5
# Convergence limit for the total clearance. AA will not converge until the total clearance is below this value.
max_total_clearance = 0.0001
# Convergence limit for the specific clearance. AA will not converge until the largest specific clearance is below this
# value.
max_specific_clearance = 0.01

# Pattern for activities that are importers and those that are exporters
# "%" is used as a generic wildcard, matching zero or more characters.
#importer_string = "%Importer%"
#exporter_string = "%Exporter%"

# Pattern for skim files; any copies of "{yr}" will be replaced by the skim year.
skim_fname = "SkimsI"

# Column in the skims file where travel distances are stored.
distance_column = "dist_da_t_op"

# Set these to True to turn the features on in the run script/AA, False to turn them off.

# Whether to apply bounds on activity amounts at the level of groups of TAZs
aa_group_bounds = False
# Whether to stop the model run if AA doesn't match its constraints
stop_on_constraint_mismatch = True
# This is whether to use LUZs (false) or TAZs (set to true) in FloorspaceI and ActivityConstraintsI,
# and also whether to produce an ActivityLocations2.csv output file which has activity by TAZ
use_floorspace_zones = True
# Whether to update size terms for imports and exports every year
calculate_import_export_size = False

# ----------------------------------------------------------------------------------------------------------------------
# PopSyn CONFIGURATION
# ----------------------------------------------------------------------------------------------------------------------

# Name of population synthesis input file (also needs to be specified in Synth.properties file)
# You can put a file called Seed<popsyn_samples_file> in any year, or in the AllYears/Inputs folder, and it will be used
# as the seed matrix for the population synthesizer.  For example, the file could be called Seedsamples.csv
# if your samples file is called samples.csv
# A common approach is to put a Seed file in the base year directory, in which case future year population
# synthesis will continue to evolve the Output from previous years, but the base year will have a fixed
# starting point that you've defined.  Another common approach is to put a Seed file in the AllYears/Inputs folder,
# so that all population synthesis runs, regardless of year, start with the same seed.  
popsyn_samples_file = "samples_sandag.csv"

# ----------------------------------------------------------------------------------------------------------------------
# AA-SD INTEGRATION CONFIGURATION
# ----------------------------------------------------------------------------------------------------------------------

# Set these to True to turn the features on in the run script, False to turn them off.

# Whether to maintain separate space inventories for AA and SD
floorspace_calc_delta = True
# Whether to maintain separate prices for AA and SD
#use_aa_to_sd_price_ratio = False
# Whether to update construction activity size terms based on SD construction
update_construction_size_terms = False
# Whether to use an ActivitiesZonalValuesI file when updating construction size terms.
use_activities_zonal_values_i = False

# Maximum prices for each space type for AA to SD price correction
#maximum_sd_prices = None

# ----------------------------------------------------------------------------------------------------------------------
# TM CONFIGURATION
# ----------------------------------------------------------------------------------------------------------------------

# Whether to run the TM directly from the PECAS run script.
# If set to true, a run_tm.py file must be provided, based on run_tm_template.py.
# The travel model runs in the years specified by tmyears.
#use_tm = False
# ----------------------------------------------------------------------------------------------------------------------
# AA-TM INTEGRATION CONFIGURATION
# ----------------------------------------------------------------------------------------------------------------------

# Whether to load outputs for the travel model
#load_tm_totals = False
# Whether to create travel model inputs in Python/SQL
#allocate_tm_totals = False
# The years in which to produce inputs for the travel model.
# Travel model inputs are automatically produced in any years where the travel model runs according to tmyears.
travel_model_input_years = range(2012,2026) # Enter a list of years (e.g. [2015, 2025, 2035]) or leave empty to turn off
# Whether to produce employment counts
#employment = False
# The base year employment to use in future employment allocation
#base_employment_fname = None # Enter a file name if employment is True
# Whether to generate trips for commercial flows (in the travel_model_input_years)
make_trip_matrices = False
# Whether to use the Poisson distribution when generating commercial trips (if make_trip_matrices is True)
poisson_trips = True
# Whether to produce trip tables in the Emme "IJV" format in addition to at trip list (if make_trip_matrices is True)
emme_format_trips = False


# Whether to squeeze skims by TAZ from the travel model up to the LUZ level
squeeze_skims = False
# The name of the TAZ skim file (if squeeze_skims is True); any copies of "{yr}" will be replaced by the skim year
taz_skims_fname = "TMSkims"

# ----------------------------------------------------------------------------------------------------------------------
# JAVA SETTINGS
# ----------------------------------------------------------------------------------------------------------------------

# PECAS jar file names, which must match the jars in AllYears/Code
pecasjar = "PecasV2.11_r9252.jar"
commonbasejar = "common-base_r7007.jar"
simpleormjar = "simple_orm_r3004.jar"
popsynjar = "population-synthesizer-8890.jar"


# Other Java settings
profiling = False
missionControl = True

# FloorspaceI column names
flItaz = "TAZ"
flIcommodity = "Commodity"
flIquantity = "Quantity"

run_supply = True
run_demand = False

update_techopt = True
update_inputs = True

