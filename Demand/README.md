# Bid-rent evaluation of demand for SRF System

The demand portion of the SRF System evaluates the MGRA-level real estate supply stock developed by the Supply model and the LUZ-level control totals provided by AA using a bid-rent framework. The R scripts in the "R" folder orchestrate this process and provide an interface to the mu-land program including an algorithm that solves for equilibrium in both residential and non-residential markets. Because there are 229 separate sets of control totals (one for each LUZ), the problem is tiled geographically into a set of sub-problems that can be solved more quickly using parallel processing.

## Prerequisites

The "mu-land" program developed as part of the Alpaca project funded by the Lincoln Insitute for Land Policy must be compiled and installed on your computer. Instructions can be found at the GitHub repository for that software:
https://github.com/ManhanGroup/Alpaca

Alternatively, contact Manhan Group, LLC (info@manhangroup.com) to obtain a pre-compiled mu-land binary executable for your system.

3. As an alternative to 2), Run the demand model in command prompt window:
   cd E:\PECAS\SRF\trunk\Demand
   "C:\Program Files\R\R-4.0.2\bin\R.exe" CMD BATCH .\R\evalDemand.R  
    Or
   "C:\Program Files\R\R-4.0.2\bin\Rscript.exe" .\R\evalDemand.R  
   R must also be installed on your system; version 3.5.0 was used to develop the associated scripts for Demand. You can learn more and download R from:
   https://www.r-project.org/

The following libraries are also required:

- yaml
- RPostgreSQL
- dplyr
- reshape2
- foreach
- doParallel

To install these, type "R" at the command line. Then, type:

<code>install.packages(c("yaml","RPostgreSQL","dplyr","reshape2","foreach","doParallel"))</code>

To exit the R prompt, type "q()" and press Enter.

## Input data

All input tables are stored in a secure database to ensure data integrity. Please contact SANDAG to obtain database access credentials.

## Running Demand

The evalDemand.R script is used to launch and orchestrate runs. It is designed to be run from the command line, in the main "Demand" folder, with an "R" subfolder containing evalDemand.R, defaultFunctions.R, helperFunctions.R, and runMuLand.R, which calls "mu-land.exe". The path to the mu-land program, wherever it is installed, must be included in your system PATH environment variable.

The general command-line syntax is as follows:
<code>rscript R\evalDemand.R path-to-dbparams name-of-scenario</code>

Normally, your dbparams.yaml file should be found in the directory above Demand. Thus, an example of typical usage might be as follows:

<code>rscript R\evalDemand.R .. Base</code>

## Output data

Demand will create a folder with the same name as the scenario you specified, with sub-folders containing inputs and outputs for each LUZ, as well as a combined_rents.csv and combined_location.csv, giving output data required to create inputs to the Supply model and SANDAG population synthesizer, respectively.
