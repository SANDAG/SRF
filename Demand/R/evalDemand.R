## Evaluate SRF System demand models
## Author: Manhan Group LLC
## Client: SANDAG
## Command-line arguments:
## 1) location of dbparams.yaml
## 2) scenario name (used to create output folder)
## Example call:
## rscript R\evalDemand.R .. base2012
## Note: output folder will contain sub-folders for each LUZ-specific sub-model
## It will also contain combined_location.csv and combined_rents.csv (region-wide results)
start_time <- Sys.time()
args <- commandArgs(trailingOnly = TRUE)
## global parameters
configDir = args[1]
scenario = args[2]
year = ifelse(is.null(args[3]),NA,args[3])
## check results if updated to latest tidyverse library
library(dplyr)
dplyr.summarise.inform = FALSE
## uses foreach and doParallel to speed up execution by distributing across available cores
source(file.path("R","runMuLand.R"))
source(file.path("R","defaultFunctions.R"))
source(file.path("R","helperFunctions.R"))
## MGRA-LUZ lookup
MGRAs <- loadMGRA(configDir,'mgra')
# list the names of data to be subset
data_frames <- c("agents_zones","bids_adjustments","demand_exogenous_cutoff","rent_adjustments","subsidies","supply","zones","real_estates_zones")
# calls function from helperFunctions to pull data from the database
# the configDir is currently the parent folder, where the file dbparams.yaml lives
master_data <- loadDemandInputs(configDir,year)
supply_data <- read.csv(file.path("..","Supply","data",paste0("forecasted_year_",year,".csv")))
master_data[["real_estates_zones"]] <- master_data[["real_estates_zones"]] %>%
  left_join(select(supply_data,MGRA,sf_new_mea,sf_old_mea,mf_new_mea,mf_old_mea),
            by=c("I_IDX"="MGRA")) %>%
  mutate(is_old = ifelse(V_IDX==1,sf_old_mea,ifelse(V_IDX==2,mf_old_mea,0)),
         is_new = ifelse(V_IDX==1,sf_new_mea,ifelse(V_IDX==2,mf_new_mea,0))) %>%
  select(-sf_new_mea,-sf_old_mea,-mf_new_mea,-mf_old_mea)
if (!dir.exists(scenario)) {
  dir.create(scenario)
}
setwd(scenario)
library(foreach)
library(doParallel)
nodes <- detectCores()-1
c1 = makeCluster(nodes)
registerDoParallel(c1)
# foreach by default creates a vector of the return results - bind_rows combines into a single data frame
loop_result <- foreach (luz=1:229, .packages=c("dplyr","reshape2"), .errorhandling='stop', .combine='bind_rows') %dopar% {
# for (luz in 1:229) {
  print(paste("Processing LUZ",luz))
  luz_dir <- paste0("LUZ_",luz)
  LUZ_MGRAs = filter(MGRAs, LUZ == luz)[["MGRA"]]
  luz_model <- list()
  # load up the data that doesn't need to be filtered
  luz_model[["agents"]] <- master_data[["agents"]]
  luz_model[["bids_functions"]] <- master_data[["bids_functions"]]
  luz_model[["rent_functions"]] <- master_data[["rent_functions"]]
  # filter other data
  luz_model[["demand"]] <- select(filter(master_data[["demand"]],LUZ==luz),-LUZ)
  for (df in data_frames) {
    luz_model[[df]] <- filter(master_data[[df]],I_IDX %in% LUZ_MGRAs)
  }
  model_out <- fsRun(luz_model,luz_dir)
  ## uses summary function from helperFunctions.R
  summaryData <- getSummary(luz_model,model_out)
  write.csv(summaryData,file.path(luz_dir,"summaryData.csv"),row.names = FALSE)
  return(model_out$location)
}
## Combine rents
rents_master <- list() # list to gather rent outputs
summary_master <- list() # list to gather summary outputs
for (luz in 1:229) {
    luz_dir <- paste0("LUZ_",luz)
    rents_master[[luz]] <- read.table(file.path(luz_dir,"output","rents.csv"),sep=";",header=TRUE)
    summary_master[[luz]] <- read.csv(file.path(luz_dir,"summaryData.csv"))
    unlink(file.path(luz_dir,"summaryData.csv"))
}
combined_rents <- bind_rows(rents_master) %>% arrange(Zone,Realestate)
combined_summary <- bind_rows(summary_master) %>% arrange(Zone)
setwd("..")
write.csv(combined_rents,file.path(scenario,"combined_rents.csv"),row.names = FALSE)
write.csv(combined_summary,file.path(scenario,"combined_summary.csv"),row.names = FALSE)
combined_location <- loop_result %>% arrange(Zone,Realestate)
write.csv(combined_location,file.path(scenario,"combined_location.csv"),row.names = FALSE)
# stop the cluster -- this might not actually be necessary
stopCluster(c1)
# Report run time
end_time <- Sys.time()
duration <- round(end_time - start_time,digits=2)
print(paste(duration,"minutes elapsed using",nodes,"nodes"))
