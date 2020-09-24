loadDemandInputs <- function(configDir,tables) {
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
    mysql <- paste0("select * from ",inputs_schema,".", table)
    d <- tryCatch(dbGetQuery(conn,mysql), error=function(e) print(paste0("Input table ",table," doesn't exists!")))
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
