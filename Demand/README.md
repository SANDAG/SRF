# Bid-rent evaluation of demand for SRF System
The demand portion of the SRF System evaluates the MGRA-level real estate supply stock developed by REDM and the LUZ-level control totals provided by AA using a bid-rent framework.  The R scripts in the "R" folder orchestrate this process and provide an interface to the mu-land program.  These scripts reference a "master" directory which must be populated from an input database.

Follow steps below to run the demand model:
1) Change the first line of evalDemand.R to point to the current directory
For example: setwd("E:/PECAS/SRF/trunk/Demand")

2) start "R"

4) Type the following to run demand model
 source("E:/PECAS/SRF/trunk/Demand/R/evalDemand.R")