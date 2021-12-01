### PECAS Activity Allocation (AA) Model
============================
The only PECAS functionalilty used by SANDAG's SRF System is the AA module, which allocates projected economic activity within San Diego County among 229 coarse Land Use Zones (LUZs) based upon a spatial input-output framework. The AA implementation provided in this Github repository (S28_aa) was extracted from a previously developed reference run of PECAS (i.e. S28). 

### System requirements and installation notes
============================
AA was developed using a combination of Java and Python.

The Anaconda distribution of Python 3 is recommended. 
Most Python packages used by the model are already included in the Anaconda default installation. You should only need to install the psycopg2 python package by running:
  `conda install psycopg2`
  
The PECAS AA model java code was compiled with Java 10, so make sure your Java version is 10 or higher. 

Check *machine_settings.py* to make sure correct paths are set for pgpath, javaRunCommand, and pythonCommand.


### Data Folder Structure
============================
Up to date data files will be downloaded from the PostgreSQL database. Alternatively you can provide the same files and copy those in the corresponding directory.

If an input file preexists in either the yearly folder or the inputs folder, it will not be downloaded again from the database. 

Hence, in order for a fresh copy of data to be downloaded, delete the pre-existing files first. 

Inputs used for the AA module for a selected year are distributed in four folders: the skim year folder,  the previous year's folder, the current year's folder and the AllYears/Inputs folder. 

#### Skim year folder
"SkimsI.csv" is located here. Check the "skimyears" defined aa_setting.py to find out the corresponding skim year folder for the current selected year for an AA model run.

#### Current year folder
"ActivityTotalsI.csv" and "FloorspaceO.csv" are required inputs.
"FloorspaceCalc.csv" will be used if it exists in the current year folder. If not, "FloorspaceDelta.csv" must exist in the previous year folder, which will be copied into the current year folder by the AA module and used.
"ExchangeResultsI.csv" are also required inputs. if "ExchangeResultsI.csv" is missing in the current folder, AA module will try to find it in the previous year folder.

#### Previous year folder
When running the AA module for a selected current year, the model will try to look for "ActivityLocations.csv" in the previous year folder. 
If not found, S28_aa model will still run and generate "ActivityLocations.csv" for the current year.

#### AllYears/Inputs folder
The following files are required in the AA module run of any selected year:
"aa.properties", "ActivitiesI.csv","ActivitySizeTermsI.csv","CommoditiesI.csv","FloorspaceSupplyI.csv", "FloorspaceZonesI.csv",
"ExchangeImportExportI.csv","HistogramsI.csv","PECASZonesI.csv","TechnologyOptionsI.csv"

For "ActivitySizeTermsI.csv", "ExchangeImportExportI.csv", "CommoditiesI.csv", "LogsumsI.csv", and "PopSynConnection.csv",
the model will look in the current year folder first before searching in the AllYears\Inputs folder.

In addition,  the AA run will try to look for "PopSynBaseTargets" in the current year folder, 
without this the population synthesizer target will not be generated. 
Also, create an empty Outputsamples_sandag.csv in AllYears\Working\PopulationSynthesis folder, 
if the file doesn't exist there yet before starting an AA model run.

### Parameter Configuration
============================
Change program inputs parameters e.g., `aa_startyear`, `stopyear`, in "aa_settings.py" accordingly.

If you need to download inputs data in the AllYears/Inputs diretory, remove the all CSV files (except "TechnologyOptionsI_header.csv") in the Inputs folder.
Then, set the following parameters in aa_settings.py to True:

`update_techopt = True`

`update_inputs = True`

If you want to rerun the squeeze skim, set the following parameter to True:
squeeze_skims = True

To update the yearly data, you can copy the new data into the yearly data folder. The program will not try to download the data from the PostgreSQL database if an existing file is found in this folder. If you removed the data in the yearly folder or the folder itself, the folder will be created and data will be downloaded from the PostgreSQL database.

### Execution
============================
Run with `python run_aa_allyears.py` to start the integrated model run, including: MU Land Supply Model, PECAS AA module, and mu-Land Demand Model
from `aa_startyear` to `stopyear` specified in the "aa_settings" file.

One can also run the PECAS AA module separately for one individual year, e.g., 2017, with `python run_aa.py 2017`.

You can reset `squeeze_skims` to `True` to run the squeeze skims process as part of the integrated model run.

In the current run_aa_allyears.py, the squeeze skim process are coded on line 135 :
          `skims_to_sem_main(skimyear, ps)`

The squeeze skim process can also be run for an individual year, e.g., 2016,  with `python skims_to_sem.py 2016`.

To run the squeeze skims process, those *.omx input files listed before need to be copied into the corresponding skim year folder first. In addition, the schema for the storage of intermedite squeeze skim results needs to exist in the postgreSQL database and the user specified in "dbparams.yaml" needs to have written permission to the database schema specified as `sd_schema` in "aa_settings.py". 

This process is time consuming and only needs to be rerun when there are new input files, 
i.e. "traffic_skims_AM.omx", "traffic_skims_MD.omx", and "transit_skims.omx".
 
Hence, you may want to keep the parameter `squeeze_skims` to `False` and run the squeeze skim process for individual years.
 


