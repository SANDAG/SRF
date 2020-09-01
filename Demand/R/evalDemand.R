setwd(".")

## global parameters
calibration = FALSE
scenario = "getRawRent"
##


library(dplyr)
library(foreign)
## MGRA-LUZ lookup
# MGRAs <- read.dbf("MGRA/MGRA.dbf",as.is = TRUE)

source(file.path("R","runMuLand.R"))
source(file.path("R","defaultFunctions.R"))
MGRAs <- loadMGRA('..','mgra')
agentCheck <- function(dfList_in,dfList_out,targets) {
  require(dplyr)
  require(reshape2)
  totalAgents <- select(reshape(dfList_out[["location"]], direction = "long", varying = 3:46),
                        V_IDX = Realestate,
                        I_IDX = Zone,
                        H_IDX = time,
                        agents = H_Type) %>%
    group_by(I_IDX,H_IDX) %>%
    summarise(NLOC = sum(agents))
  checkAgents <- rbind(
    left_join(totalAgents,dfList_in$agents,by=c("H_IDX"="IDAGENT")) %>%
      filter(IDMARKET==1) %>%
      group_by(I_IDX,IDAGGRA) %>%
      summarise(sumAgents = sum(NLOC)) %>%
      mutate(sumAgents = sumAgents + 0.0001) %>%
      select(I_IDX,calGroup=IDAGGRA,sumAgents),
    left_join(totalAgents,dfList_in$agents,by=c("H_IDX"="IDAGENT")) %>%
      filter(IDMARKET==2) %>%
      mutate(calGroup=H_IDX-10) %>%
      group_by(I_IDX,calGroup) %>%
      summarise(sumAgents = sum(NLOC)) %>%
      mutate(sumAgents = sumAgents + 0.0001)
  ) %>%
    arrange(I_IDX,calGroup) %>%
    left_join(
      mutate(
        melt(targets,id.vars=1,measure.vars=2:35,value.name="TARGET"),
        calGroup = as.numeric(variable),
        TARGET = TARGET + 0.0001
      ),
      by=c("I_IDX"="mgra","calGroup"="calGroup")
    ) %>%
    mutate(err = sumAgents - TARGET,
           ape = 100*abs(err / TARGET),
           sqr = err**2,
           adj = log(TARGET/sumAgents)
    )
  return(checkAgents)
}

fsCal <- function(inputDfList, workDir='fsCal', targets, endogFn=nullEndogFn, tol=5.0, maxiters=10){
  progress=vector("list",maxiters)
  for (k in 1:maxiters){
    outputDfList <- fsRun(inputDfList, workDir, createDir = TRUE, endogFn = endogFn)
    checkAgents <- agentCheck(inputDfList,outputDfList,targets)
    cal_WAAPE = 100*sum(abs(checkAgents$err))/sum(checkAgents$TARGET)
    # avgAPE = mean(checkAgents$ape)
    progress[k] <- cal_WAAPE
    print(paste("Outer iteration",k,"weighted avg. absolute percent error =",cal_WAAPE))
    if (cal_WAAPE < tol) {
      print("Calibration converged, exiting...")
      print(paste(progress,sep="\n"))
      break
    } else {
      inputDfList$bids_adjustments <- inputDfList$bids_adjustments %>%
        left_join(inputDfList$agents, by=c("H_IDX"="IDAGENT")) %>%
        mutate(calGroup = ifelse(IDMARKET==1,IDAGGRA,H_IDX-10)
        ) %>% 
        left_join(checkAgents, by = c("I_IDX"="I_IDX","calGroup"="calGroup")) %>%
        transmute(H_IDX = H_IDX,
                  V_IDX = V_IDX,
                  I_IDX = I_IDX,
                  BIDADJ = BIDADJ + adj)
      inputDfList <- endogFn(inputDfList,outputDfList)
    }
  }
  return(inputDfList[["bids_adjustments"]])
}
# list the names of data to be subset
data_frames <- c( "agents_zones","bids_adjustments","demand_exogenous_cutoff","rent_adjustments","subsidies","supply","zones","real_estates_zones")

# store input dataframes in a list
#master_data <- list()
# loop over these names to load those data
#for (df in data_frames) {
 # master_data[[df]] <- read.csv(file.path("master",paste0(df,"_master.csv"))) 
#}

master_data <- loadMuLandInputs('..')


# start looping over the LUZs
if (calibration == TRUE) {
  bidAdj_master <- list()
} else {
  rents_master <- list() # list to gather rent outputs
  location_master <- list() # list to gather location output tables
}
if (!dir.exists(scenario)) {
  dir.create(scenario)  
}
setwd(scenario)
for (luz in 1:229) {
  print(paste("Processing LUZ",luz))
  luz_dir <- paste0("LUZ_",luz)
  LUZ_MGRAs = filter(MGRAs, LUZ == luz)[["MGRA"]]
  luz_model <- list()
  # load up the data that doesn't need to be filtered
  luz_model[["agents"]] <- master_data[["agents"]]
  luz_model[["bids_functions"]] <- master_data[["bids_functions"]]
  #luz_model[["rent_functions"]] <- master_data[["rent_functions_0"]]
  luz_model[["rent_functions"]] <- master_data[["rent_functions"]]
  # filter other data
  luz_model[["demand"]] <- select(filter(master_data[["demand"]],LUZ==luz),-LUZ)
  for (df in data_frames) {
    luz_model[[df]] <- filter(master_data[[df]],I_IDX %in% LUZ_MGRAs)
  }
  if (calibration==TRUE) {
    luz_targets <- filter(targets,mgra %in% LUZ_MGRAs)
    luz_bidAdj <- fsCal(luz_model,luz_dir,luz_targets)
    bidAdj_master[[luz]] <- luz_bidAdj
  } else {
    model_out <- fsRun(luz_model,luz_dir)
    rents_master[[luz]] <- model_out$rents
    location_master[[luz]] <- model_out$location
  }
}
setwd("..")
if (calibration==TRUE) {
  master_data[["bids_adjustments"]] <- bind_rows(bidAdj_master) %>%
    arrange(V_IDX,I_IDX,H_IDX)
  write.csv(master_data[["bids_adjustments"]],file.path("master","bids_adjustments_master.csv"),row.names = FALSE)
} else {
  combined_rents <- bind_rows(rents_master) %>%
    arrange(Zone,Realestate)
  write.csv(combined_rents,file.path(scenario,"combined_rents.csv"),row.names = FALSE)
  combined_location <- bind_rows(location_master) %>%
    arrange(Zone,Realestate)
  write.csv(combined_location,file.path(scenario,"combined_location.csv"),row.names = FALSE)
}
