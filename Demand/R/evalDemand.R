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
year = as.integer(scenario) # ifelse(is.null(args[3]),NA,args[3])
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
supply_data <- read.csv(file.path("..","PostProcessor","Data",paste0("forecasted_year_",year,".csv")))
mgra13_base <- read.csv(file.path("..","PostProcessor","Data",paste0("mgra13_based_input",(year-1),".csv")))
master_data[["real_estates_zones"]] <- master_data[["real_estates_zones"]] %>%
  left_join(select(supply_data,MGRA,sf_new_mea,sf_old_mea,mf_new_mea,mf_old_mea),
            by=c("I_IDX"="MGRA")) %>%
  mutate(is_old = ifelse(V_IDX==1,sf_old_mea,ifelse(V_IDX==2,mf_old_mea,0)),
         is_new = ifelse(V_IDX==1,sf_new_mea,ifelse(V_IDX==2,mf_new_mea,0))) %>%
  select(V_IDX,I_IDX,M_IDX,is_SF,is_MF,is_MH,is_old,is_new,avg_beds,ln_rooms,is_ind,is_com,is_ofc,sf_emp,FAR,sqft_du)
master_data[["supply"]] <- master_data[["supply"]] %>%
  left_join(select(supply_data,MGRA,hs_sf,hs_mf,hs_mh,industrial_js,commercial_js,office_js),
            by=c("I_IDX"="MGRA")) %>%
  mutate(NREST = (V_IDX==1)*hs_sf+(V_IDX==2)*hs_mf+(V_IDX==3)*hs_mh+(V_IDX==4)*industrial_js+(V_IDX==5)*commercial_js+(V_IDX==6)*office_js) %>%
  select(-hs_sf,-hs_mf,-hs_mh,-industrial_js,-commercial_js,-office_js)

if (year > 2013) {
  master_data[["zones"]] <- read.csv(file.path(year-1,"zones_master.csv"))
  if (file.exists(file.path("data",paste0("accessibilities_",year,".csv")))) {
    updated_access_df <- read.csv(file.path("data",paste0("accessibilities_",year,".csv")))
    # gotta make sure they're the same length & in the same order
    if (dim(updated_access_df)[1]!=dim(master_data[["zones"]])[1]) stop("updated accessibility table has wrong number of rows")
    updated_access_df <- updated_access_df %>% arrange(MGRA)
    master_data[["zones"]] <- arrange(master_data[["zones"]],"I_IDX")
    access_cols <- c("NONMAN_AUTO","NONMAN_TRANSIT","NONMAN_NONMOTOR","ATWORK_SOV_0","ATWORK_SOV_2","TOTAL_EMP","ATWORK_NM","ALL_HHS_TRANSIT")
    master_data[["zones"]][4:11] <- updated_access_df[access_cols]
  }
}
master_data[["zones"]] <- master_data[["zones"]] %>%
  left_join(select(supply_data,MGRA,dev_indus,dev_comm,dev_office,dev_oth), by=c("I_IDX"="MGRA")) %>%
  left_join(select(mgra13_base,mgra,acres,empden,retempden,popden,duden,
                   i7,i8,i9,i10), by=c("I_IDX"="mgra"),suffix=c('.old','.new')) %>%
  mutate(shr_ind_acres = dev_indus / acres,
         shr_com_acres = dev_comm / acres,
         shr_ofc_acres = dev_office / acres,
         shr_oth_acres = dev_oth / acres,
         highIncAcre = (i7 + i8 + i9 + i10)/acres,
         duden = duden.new,
         popden = popden.new,
         emp_density = empden,
         retempden = retempden.new
         ) %>%
  select(I_IDX,ONE,TEN,NONMAN_AUTO,NONMAN_TRANSIT,NONMAN_NONMOTOR,ATWORK_SOV_0,ATWORK_SOV_2,TOTAL_EMP,ATWORK_NM,ALL_HHS_TRANSIT,
         highIncAcre,emp_density,shr_ind_acres,shr_com_acres,shr_ofc_acres,shr_oth_acres,duden,popden,retempden,
         milestocoast,pct_park,pct_beach,int_density,dparkcost)
if (!dir.exists(scenario)) {
  dir.create(scenario)
}
write.csv(master_data[["zones"]],file.path(scenario,paste0("zones_master.csv")),row.names = FALSE) # for accessibility updates
write.csv(master_data[["real_estates_zones"]],file.path(scenario,paste0("REZ_master.csv")),row.names = FALSE) # mainly for debug
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
  ## summary function - also from helperFunctions.R
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
