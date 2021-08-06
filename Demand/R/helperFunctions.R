

loadDemandInputs <- function(configDir,year,tables) {
  library(yaml)
  config_file = file.path(configDir, "dbparams.yaml")
  config <- yaml.load_file(config_file)
  
  library(RPostgreSQL)
  m <- dbDriver('PostgreSQL')
  conn <- dbConnect(m, host=config$host, dbname=config$database, user=config$user, password=config$password, port=config$port)
  on.exit(dbDisconnect(conn))
  inputs_schema <- config$mu_schema
  mysql <- paste0("select schema_name FROM information_schema.schemata WHERE schema_name = '", inputs_schema,"';")
  tryCatch(dbSendQuery(conn,mysql), error=function(e) print("Input schema doesn't exists!"))
  
  # create vector of necessary tables
  if (missing(tables)){
    tables <- c("agents",
                "agents_zones",
                "bids_adjustments",
                "bids_functions",
                "demand",
                "demand_exogenous_cutoff",
                "real_estates_zones",
                "rent_adjustments",
                "rent_functions",
                "subsidies",
                "supply",
                "zones")
  }
  
  # load csv files into inputList
  inputList <- list()
  for (table in tables) {
    if (table!="demand" || is.na(year)){
      mysql <- paste0("select * from ",inputs_schema,".", table)
    } else {
      mysql <- paste0('select * from ',inputs_schema,'.demand_', year,' d1 union select d.* from ',
                      inputs_schema,'.demand d left join ',inputs_schema,'.demand_', year,
                      ' d1 on d."LUZ"= d1."LUZ" and d."H_IDX"=d1."H_IDX" where d1."LUZ" is null order by "LUZ", "H_IDX";')
    }
    #print(mysql)
    d <- tryCatch(dbGetQuery(conn,mysql), error=function(e) print(paste0("Input table ",table," doesn't exists!")))
    #print(dim(d))
    inputList[[table]] <- d
    
  }
  
  return(inputList)
  
}

loadMGRA <- function(configDir,tname) {
  library(yaml)
  config_file = paste0(configDir, "/dbparams.yaml")
  config <- yaml.load_file(config_file)
  
  library(RPostgreSQL)
  m <- dbDriver('PostgreSQL')
  conn <- dbConnect(m, host=config$host, dbname=config$database, user=config$user, password=config$password, port=config$port)
  on.exit(dbDisconnect(conn))
  inputs_schema <- config$mu_schema
  mysql <- paste0("select table_name FROM information_schema.tables WHERE table_schema='", inputs_schema,"' and table_name = '", tname,"';")
  tryCatch(dbSendQuery(conn,mysql), error=function(e) print("Input Table doesn't exists!"))
  
  # load data from pg
  mysql <- paste0('select mgra as "MGRA", luz as "LUZ", acres as ACRES from ',inputs_schema,'."', tname,'"')
  d <- tryCatch(dbGetQuery(conn,mysql), error=function(e) print(paste0("Input table ",table," doesn't exists!")))
  
  
  return(d)
  
}

loadaa2demandinputs <- function(configDir,tname) {
  library(yaml)
  config_file = paste0(configDir, "/dbparams.yaml")
  config <- yaml.load_file(config_file)
  
  library(RPostgreSQL)
  m <- dbDriver('PostgreSQL')
  conn <- dbConnect(m, host=config$host, dbname=config$database, user=config$user, password=config$password, port=config$port)
  on.exit(dbDisconnect(conn))
  inputs_schema <- config$mu_schema
  mysql <- paste0("select table_name FROM information_schema.tables WHERE table_schema='", inputs_schema,"' and table_name = '", tname,"';")
  tryCatch(dbSendQuery(conn,mysql), error=function(e) print("Input Table doesn't exists!"))
  
  # load data from pg
  mysql <- paste0('select * from ',inputs_schema,'."', tname,'"')
  d <- tryCatch(dbGetQuery(conn,mysql), error=function(e) print(paste0("Input table ",table," doesn't exists!")))
  
  return(d)
  
}

writeaa2demandoutputs <- function(configDir,tname, mydf) {
  library(yaml)
  config_file = paste0(configDir, "/dbparams.yaml")
  config <- yaml.load_file(config_file)
  
  library(RPostgreSQL)
  m <- dbDriver('PostgreSQL')
  conn <- dbConnect(m, host=config$host, dbname=config$database, user=config$user, password=config$password, port=config$port)
  on.exit(dbDisconnect(conn))
  inputs_schema <- config$mu_schema
  mytbl <- c(inputs_schema, tname)
  # #if(dbExistsTable(conn, mytbl)){ dbRemoveTable(conn, mytbl)}
  # sql_truncate <- paste("TRUNCATE ", paste(inputs_schema,tname,sep=".")) ##unconditional DELETE FROM�
  # dbSendQuery(conn, statement=sql_truncate)
  # dbWriteTable(conn, mytbl,mydf, row.names=FALSE, append=TRUE)
  if(dbExistsTable(conn, mytbl)){
    sql_truncate <- paste("TRUNCATE ", paste(inputs_schema,tname,sep=".")) ##unconditional DELETE FROM�
    dbSendQuery(conn, statement=sql_truncate)
  }
  dbWriteTable(conn, mytbl,mydf, row.names=FALSE, append=TRUE)
}

## function to pull an arbitrary table
loadPGTbl <- function(configDir,tname) {
  library(yaml)
  config_file = paste0(configDir, "/dbparams.yaml")
  config <- yaml.load_file(config_file)
  
  library(RPostgreSQL)
  m <- dbDriver('PostgreSQL')
  conn <- dbConnect(m, host=config$host, dbname=config$database, user=config$user, password=config$password, port=config$port)
  on.exit(dbDisconnect(conn))
  inputs_schema <- config$mu_schema
  mysql <- paste0("select table_name FROM information_schema.tables WHERE table_schema='", inputs_schema,"' and table_name = '", tname,"';")
  tryCatch(dbSendQuery(conn,mysql), error=function(e) print("Input Table doesn't exists!"))
  
  # load data from pg
  mysql <- paste0('select * from ',inputs_schema,'."', tname,'"')
  d <- tryCatch(dbGetQuery(conn,mysql), error=function(e) print(paste0("Input table ",table," doesn't exists!")))
  
  
  return(d)
  
}

agentCheck <- function(location,targets) {
  require(dplyr)
  require(reshape2)
  totalAgents <- transmute(melt(location,
                                id.vars=c("Realestate","Zone"),
                                measure.vars=3:52),
                           V_IDX = Realestate,
                           I_IDX = Zone,
                           H_IDX = as.numeric(variable),
                           agents = value) %>%
    group_by(I_IDX,H_IDX) %>%
    summarise(NLOC = sum(agents))
  checkAgents <- totalAgents %>%
    group_by(I_IDX,H_IDX) %>%
    summarise(sumAgents = sum(NLOC)) %>%
    mutate(sumAgents = sumAgents + 0.0001) %>%
    arrange(I_IDX,H_IDX) %>%
    left_join(
      mutate(
        melt(targets,id.vars=1,measure.vars=2:51,value.name="TARGET"),
        H_IDX = as.numeric(variable),
        TARGET = TARGET + 0.0001
      ),
      by=c("I_IDX"="mgra","H_IDX"="H_IDX")
    ) %>%
    mutate(err = sumAgents - TARGET,
           ape = 100*abs(err / TARGET),
           sqr = err**2,
           adj = log(TARGET/sumAgents)
    )
  return(checkAgents)
}

# function to produce data for updating summary file
getSummary <- function(inputList,outputList) {
  agent_data <- inputList[["agents"]]
  # supply_data <- inputList[["supply"]]
  loc_output <- outputList[["location"]]
  summary_data <- summarise(group_by(mutate(loc_output,
                                            hh = H_Type.1. + H_Type.2. + H_Type.3. + H_Type.4. + H_Type.5. +
                                              H_Type.6. + H_Type.7. + H_Type.8. + H_Type.9. + H_Type.10. +
                                              H_Type.11. + H_Type.12. + H_Type.13. + H_Type.14. + H_Type.15. +
                                              H_Type.16. + H_Type.17. + H_Type.18. + H_Type.19. + H_Type.20.,
                                            hh_sf = ifelse(Realestate==1,hh,0),
                                            hh_mf = ifelse(Realestate==2,hh,0),
                                            hh_mh = ifelse(Realestate==3,hh,0)),Zone),
                            hh = sum(hh),
                            hh_sf = sum(hh_sf),
                            hh_mf = sum(hh_mf),
                            hh_mh = sum(hh_mh),
                            hhinc1s1 = sum(H_Type.1.),
                            hhinc1s2 = sum(H_Type.2.),
                            hhinc2s1 = sum(H_Type.3.),
                            hhinc2s2 = sum(H_Type.4.),
                            hhinc3s1 = sum(H_Type.5.),
                            hhinc3s2 = sum(H_Type.6.),
                            hhinc4s1 = sum(H_Type.7.),
                            hhinc4s2 = sum(H_Type.8.),
                            hhinc5s1 = sum(H_Type.9.),
                            hhinc5s2 = sum(H_Type.10.),
                            hhinc6s1 = sum(H_Type.11.),
                            hhinc6s2 = sum(H_Type.12.),
                            hhinc7s1 = sum(H_Type.13.),
                            hhinc7s2 = sum(H_Type.14.),
                            hhinc8s1 = sum(H_Type.15.),
                            hhinc8s2 = sum(H_Type.16.),
                            hhinc9s1 = sum(H_Type.17.),
                            hhinc9s2 = sum(H_Type.18.),
                            hhinc10s1 = sum(H_Type.19.),
                            hhinc10s2 = sum(H_Type.20.),
                            emp_ag = sum(H_Type.21.),
                            emp_const_non_bldg_prod = sum(H_Type.22.),
                            emp_const_non_bldg_office = sum(H_Type.23.),
                            emp_utilities_prod = sum(H_Type.24.),
                            emp_utilities_office = sum(H_Type.25.),
                            emp_const_bldg_prod = sum(H_Type.26.),
                            emp_const_bldg_office = sum(H_Type.27.),
                            emp_mfg_prod = sum(H_Type.28.),
                            emp_mfg_office = sum(H_Type.29.),
                            emp_whsle_whs = sum(H_Type.30.),
                            emp_trans = sum(H_Type.31.),
                            emp_retail = sum(H_Type.32.),
                            emp_prof_bus_svcs = sum(H_Type.33.),
                            emp_prof_bus_svcs_bldg_maint = sum(H_Type.34.),
                            emp_pvt_ed_k12 = sum(H_Type.35.),
                            emp_pvt_ed_post_k12_oth = sum(H_Type.36.),
                            emp_health = sum(H_Type.37.),
                            emp_personal_svcs_office = sum(H_Type.38.),
                            emp_amusement = sum(H_Type.39.),
                            emp_hotel = sum(H_Type.40.),
                            emp_restaurant_bar = sum(H_Type.41.),
                            emp_personal_svcs_retail = sum(H_Type.42.),
                            emp_religious = sum(H_Type.43.),
                            emp_pvt_hh = sum(H_Type.44.),
                            emp_state_local_gov_ent = sum(H_Type.45.),
                            emp_fed_non_mil = sum(H_Type.46.),
                            emp_fed_mil = sum(H_Type.47.),
                            emp_state_local_gov_blue = sum(H_Type.48.),
                            emp_state_local_gov_white = sum(H_Type.49.),
                            emp_public_ed = sum(H_Type.50.)) %>%
    mutate(i1 = hhinc1s1 + hhinc1s2,
           i2 = hhinc2s1 + hhinc2s2,
           i3 = hhinc3s1 + hhinc3s2,
           i4 = hhinc4s1 + hhinc4s2,
           i5 = hhinc5s1 + hhinc5s2,
           i6 = hhinc6s1 + hhinc6s2,
           i7 = hhinc7s1 + hhinc7s2,
           i8 = hhinc8s1 + hhinc8s2,
           i9 = hhinc9s1 + hhinc9s2,
           i10 = hhinc10s1 + hhinc10s2,
           hhp = hhinc1s1*agent_data$hhsize[1] +
             hhinc1s2*agent_data$hhsize[2] +
             hhinc2s1*agent_data$hhsize[3] +
             hhinc2s2*agent_data$hhsize[4] +
             hhinc3s1*agent_data$hhsize[5] +
             hhinc3s2*agent_data$hhsize[6] +
             hhinc4s1*agent_data$hhsize[7] +
             hhinc4s2*agent_data$hhsize[8] +
             hhinc5s1*agent_data$hhsize[9] +
             hhinc5s2*agent_data$hhsize[10] +
             hhinc6s1*agent_data$hhsize[11] +
             hhinc6s2*agent_data$hhsize[12] +
             hhinc7s1*agent_data$hhsize[13] +
             hhinc7s2*agent_data$hhsize[14] +
             hhinc8s1*agent_data$hhsize[15] +
             hhinc8s2*agent_data$hhsize[16] +
             hhinc9s1*agent_data$hhsize[17] +
             hhinc9s2*agent_data$hhsize[18] +
             hhinc10s1*agent_data$hhsize[19] +
             hhinc10s2*agent_data$hhsize[20])
  emp_total <- rowSums(summaryData[26:55])
  summaryData <- cbind(summaryData,emp_total)
  return(summary_data)
}

updateEndogVars_Fn <- function(inputList, outputList){
  # this is like a sneak preview of the summary created at the end of the run
  summaryData <- getSummary(inputList,outputList)
  # MGRA-based input must be loaded before following line will work
  # summaryData <- left_join(summaryData,select(mgra13_base,mgra,acres,gq_civ,gq_mil),by=c("Zone"="mgra")
  # most of the variables we need to update are densities which can't be reproduced using available area data
  # where possible, we'll incrementally adjust them using growth rates
  compareData <- left_join(summaryData,mgra13_base,by=c("Zone"="mgra"),suffix=c(".endog",".prior")) %>%
    mutate(highInc.prior = i7.prior + i8.prior + i9.prior + i10.prior,
           highInc.endog = i7.endog + i8.endog + i9.endog + i10.endog,
           pop.prior = pop,
           pop.endog = gq_civ + gq_mil + hhp.endog) %>%
    select(mgra=Zone,acres,
           highInc.prior,highInc.endog,hs.prior,hs.endog,pop.prior,pop.endog,
           emp_total.prior,emp_total.endog,emp_retail.prior,emp_retail.endog)
  compareData[is.na(compareData)] <- 0
  inputList[["zones"]] <- inputList[["zones"]] %>%
    left_join(compareData,by=c("I_IDX"="mgra")) %>%
    mutate(highIncAcre = ifelse(highInc.prior > 0, 
                                highIncAcre*(highInc.endog/highInc.prior), 
                                highInc.endog / acres),
           emp_density = ifelse(emp_total.prior > 0, 
                                emp_density*(emp_total.endog/emp_total.prior), 
                                emp_total.endog / acres),
           popden = ifelse(pop.prior > 0, 
                           popden*(pop.endog/pop.prior), 
                           pop.endog / acres),
           retempden = ifelse(emp_retail.prior > 0, 
                              retempden*(emp_retail.endog/emp_retaill.prior), 
                              emp_retail.endog / acres)
           ) %>%
    select(-c(highInc.prior,highInc.endog,hs.prior,hs.endog,pop.prior,pop.endog,
              emp_total.prior,emp_total.endog,emp_retail.prior,emp_retail.endog))
  return(inputList)
}
