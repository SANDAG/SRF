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
  mysql <- paste0('select mgra as "MGRA", luz as "LUZ" from ',inputs_schema,'."', tname,'"')
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
  #if(dbExistsTable(conn, mytbl)){ dbRemoveTable(conn, mytbl)} 
  sql_truncate <- paste("TRUNCATE ", paste(inputs_schema,tname,sep=".")) ##unconditional DELETE FROM…
  dbSendQuery(conn, statement=sql_truncate)
  dbWriteTable(conn, mytbl,mydf, row.names=FALSE, append=TRUE)
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
