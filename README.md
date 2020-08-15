# SRF
SRF Development (Sub-Regional Forecasting System)

Step 1: Contact the administrator to set up database user and modify the PostgreSQL connection information in dbparams.yaml. 

Step 2: Update machine_settings.py based on your computer's setting such as the path to java run command.

Step 3: Go to directory PECAS/S28_aa and make directory "2016" here
        Copy the travel demand model outputs: traffic_skims_AM.omx, traffic_skims_MD.omx and transit_skims.omx from
        the current model "2016" folder: https://svn.hbaspecto.com/svn/pecas/PECASSanDiego/S28/2016

Step 4: Go to directory PECAS/AllYears and make directory "Code" here
        Copy the *.jar files and hdf5 folder from the current model AllYears/Code folder: 
        https://svn.hbaspecto.com/svn/pecas/PECASSanDiego/S28/AllYears/Code .
        Also check to make sure aa.properties is in the AllYears/Inputs folder. If not, you will get aa bundle not found error.

Step 5: Run aa only model for all years by: 
        cd PECAS/S28_aa
        python run_aa_allyears.py 

Step 6: Run MU Land Supply Model by:
        cd Supply/REDM
        python redm_main.py
        
        
Step 7: Run MU Land Demand Model by:
        cd E:\PECAS\SRF\trunk\Demand
        "C:\Program Files\R\R-4.0.2\bin\R.exe" CMD BATCH .\R\evalDemand.R
        or 
         "C:\Program Files\R\R-4.0.2\bin\Rscript.exe" .\R\evalDemand.R . 
        Make sure the path to R command or Rscript command is correct.





