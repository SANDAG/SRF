# Check muLand inputs --------------------------------------------------------
#' Check inputs to muLand program
#'
#' Takes the inputs to the runMuLand R function, ensures their validity, and
#' that they contain all information necessary to run the muLand utility. This
#' includes checking the existence of and optionally creating the muLand target
#' working directory structure and validating the scenario input list. The
#' input list of data frames is validated to contain the twelve necessary data
#' frames and that each data frame contains all necessary variables allowing
#' for scenario-specific inputs where appropriate.
#' 
#' The required structure of the input list of dataframes:
#' \itemize{
#'   \item \strong{agents}{ - enumerates agent types and defines their
#'     attributes - [IDAGENT, IDMARKET, IDAGGRA, UPPERBB, (model-defined)]}
#'   \item \strong{agents_zones}{ - provides input data dimensioned by zone
#'     and agent type - [H_IDX, I_IDX, ACC, ATT, (model-defined)]}
#'   \item \strong{bids_adjustments}{ - calibration constants adjusted to fit
#'     observed base data - [H_IDX, V_IDX, I_IDX, BIDADJ]}
#'   \item \strong{bids_functions}{ - table representation of the bid
#'     functions - [IDMARKET, IDAGGRA, IDATTRIB, LINEAPAR, CAGENT_X, CREST_X,
#'     CACC_X, CZONES_X, EXPPAR_X, CAGENT_Y, CREST_Y, CACC_Y, CZONES_Y, EXPPAR_Y]}
#'   \item \strong{demand}{ - control totals of agents by type - [H_IDX, NAGENT]}
#'   \item \strong{demand_exogenous_cutoff}{ - describes which agents may
#'     compete for which units/locations - [H_IDX, V_IDX, I_IDX, DCUTOFF]}
#'   \item \strong{real_estates_zones}{ - characteristics of housing units by
#'     type and zone - [V_IDX, I_IDX, M_IDX, (model-defined)]}
#'   \item \strong{rent_adjustments}{ - calibration constants used to fit
#'     observed data - [V_IDX, I_IDX, RENTADJ]}
#'   \item \strong{rent_functions}{ - functions for estimating rents/real
#'     estate prices - [IDMARKET, IDATTRIB, SCALEPAR, LINEAPAR, CREST_X,
#'     CZONES_X, EXPPAR_X, CREST_Y, CZONES_Y, EXPPAR_Y]}
#'   \item \strong{subsidies}{ - subsidies/taxes by zone, real estate unit, or
#'     agent type - [H_IDX, V_IDX, I_IDX, SUBSIDES]}
#'   \item \strong{supply}{ - scenario-specific distribution of units by type
#'     and zone - [V_IDX, I_IDX, N_REST]}
#'   \item \strong{zones}{ - enumerates zones and defines their attributes -
#'     [I_IDX, (model-defined)]}}
#'
#'
#' @param inputList List of data frames of input to muLand program
#' @param workDir String of target muLand working directory
#' @param createDir Logical (optional) indicator of whether to create the
#'   target muLand working directory if it does not exist, defaults to TRUE
#'
#' @return Logical value indicating success (TRUE) 
#'
#' @author Manhan Group LLC
#' @export
checkMuLandInputs <- function(inputList, workDir, createDir = TRUE) {

  # create data dictionary of the elements of the input list
  # of DataFrames to the MuLand program
  # Colby to send over data model
  muLandDict <- list(
    names = 
      c("agents",
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
        "zones"),
    cols = list(
      c("IDAGENT",
        "IDMARKET",
        "IDAGGRA",
        "UPPERBB"),
      c("H_IDX",
        "I_IDX",
        "ACC",
        "ATT"),
      c("H_IDX",
        "V_IDX",
        "I_IDX",
        "BIDADJ"),
      c("IDMARKET",
        "IDAGGRA",
        "IDATTRIB",
        "LINEAPAR",
        "CAGENT_X",
        "CREST_X",
        "CACC_X",
        "CZONES_X",
        "EXPPAR_X",
        "CAGENT_Y",
        "CREST_Y",
        "CACC_Y",
        "CZONES_Y",
        "EXPPAR_Y"),
      c("H_IDX",
        "NAGENT"),
      c("H_IDX",
        "V_IDX",
        "I_IDX",
        "DCUTOFF"),
      c("V_IDX",
        "I_IDX",
        "M_IDX"),
      c("V_IDX",
        "I_IDX",
        "RENTADJ"),
      c("IDMARKET",
        "IDATTRIB",
        "SCALEPAR",
        "LINEAPAR",
        "CREST_X",
        "CZONES_X",
        "EXPPAR_X",
        "CREST_Y",
        "CZONES_Y",
        "EXPPAR_Y"),
      c("H_IDX",
        "V_IDX",
        "I_IDX",
        "SUBSIDIES"),
      c("V_IDX",
        "I_IDX",
        "NREST"),
      c("I_IDX"))
  )
  
  # check input list contains only data frames
  if(any(!sapply(X = inputList, FUN = is.data.frame))){
    stop("Not all elements of input list are data frames")
  }
  
  # for each specified DataFrame
  for(i in seq_along(muLandDict[["names"]])) {
    dfName <- muLandDict[["names"]][i]
    dfCols <- muLandDict[["cols"]][[i]]
    
    # check input list contains the specified DataFrame
    if(!dfName %in% names(inputList)){
      msg <- paste0("DataFrame '",
                    dfName,
                    "' not contained in input list")
      stop(msg)
    }
    
    # check input list data frame contains all columns specified
    if(any(!dfCols %in% names(inputList[[dfName]]))) {
      wrongCols <-
        dfCols[!dfCols %in% names(inputList[[dfName]])]
      
      msg <- paste0("DataFrame '",
                    dfName,
                    "' does not contain specified columns: ",
                    paste(wrongCols, collapse = ", "))
      
      stop(msg)
    }
  }
  
  # create the working directory if it does not exist
  # and input parameter to create was specified
  if(!dir.exists(workDir)) {
    if(createDir) {
      dir.create(workDir)
    } else {
      msg <- paste("Working directory does not exist:",
                   workDir,
                   sep = " ")
      
      stop(msg)
    }
  }
  
  # create the input sub-directory if it does not exist
  # and input parameter to create was specified
  if(!dir.exists(file.path(workDir, "input"))) {
    if(createDir) {
      dir.create(file.path(workDir, "input"))
    } else {
      msg <- paste("Input directory does not exist:",
                   file.path(workDir, "input"),
                   sep = " ")
      
      stop(msg)
    }
  }
  
  # return TRUE if all consistency checks are passed
  return(TRUE)
  
}








# Load muLand inputs ---------------------------------------------------------
#' Load inputs to muLand program
#'
#' Loads the necessary csv input files to the muLand program.
#' 
#' @param workDir String of target working directory containing csv inputs to
#'   the muLand program
#'
#' @return List of data frames of input to muLand program
#'
#' @author Manhan Group LLC
#' @export
loadMuLandInputs_csv <- function(workDir) {
  
  inputDir <- paste0(workDir, "/input/")
  
  # check if the working directory exists and the input folder exists
  if(!dir.exists(workDir)) {
    msg <- "Working directory does not exist"
    stop(msg)
  } else if (!dir.exists(inputDir)) {
    msg <- "Input folder does not exist in working directory"
    stop(msg)
  }
  
  # create vector of necessary csv files
  files <- c("agents",
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
  
  # load csv files into inputList
  inputList <- list()
  for (file in files) {
    csvFile <- paste0(inputDir, file, ".csv")
    if(!file.exists(csvFile)) {
      msg <- paste0("Input file does not exist: ",
                    csvFile)
      stop(msg)
    } else {
      inputList[[file]] <- read.table(csvFile, header=TRUE, sep=";")
    }
  }
  
  return(inputList)
  
}

loadMuLandInputs <- function(configDir,tables) {
  library(yaml)
  config_file = paste0(configDir, "/dbparams.yaml")
  config <- yaml.load_file(config_file)
  
  library(RPostgreSQL)
  m <- dbDriver('PostgreSQL')
  conn <- dbConnect(m, host=config$aa_host, dbname=config$aa_database, user=config$aa_user, password=config$aa_password, port=config$aa_port)
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
             #"rent_functions_0",
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
  conn <- dbConnect(m, host=config$aa_host, dbname=config$aa_database, user=config$aa_user, password=config$aa_password, port=config$aa_port)
  on.exit(dbDisconnect(conn))
  inputs_schema <- config$mu_schema
  mysql <- paste0("select table_name FROM information_schema.tables WHERE table_schema='", inputs_schema,"' and table_name = '", tname,"';") 
  tryCatch(dbSendQuery(conn,mysql), error=function(e) print("Input Table doesn't exists!"))
  
  # load data from pg
  mysql <- paste0('select mgra as "MGRA", luz as "LUZ" from ',inputs_schema,'."', tname,'"')
  d <- tryCatch(dbGetQuery(conn,mysql), error=function(e) print(paste0("Input table ",table," doesn't exists!")))
  
  
  return(d)
  
}

# Return muLand outputs ------------------------------------------------------
#' Read in outputs from the muLand program
#'
#' Reads the output csv files from the runMuLand R function, ensures their
#' validity, and that they contain all information necessary. The output list
#' of data frames is validated to contain the five necessary data frames and
#' that each data frame contains all necessary variables allowing for
#' scenario-specific inputs where appropriate.
#' 
#' The structure of the output list of dataframes:
#' \itemize{
#'   \item \strong{bh}{ - agent-specific adjustments to bids to equilibrate
#'     supply-demand - [Agents, Value]}
#'   \item \strong{bids}{ - bids by zone, real estate unit, and agent type -
#'     [Realestate, Zone, (model-defined)]}
#'   \item \strong{location}{ - allocated agents by zone and real estate unit
#'     type - [Realestate, Zone, (model-defined)]}
#'   \item \strong{location_probability}{ - location table expressed as
#'     shares - [Realestate, Zone, (model-defined)]}
#'   \item \strong{rents}{ - rents by real estate unit type and zone -
#'     [Realestate, Zone, Value]}}
#'
#'
#' @param inputList List of data frames of input to muLand program
#' @param workDir String of target muLand working directory
#'
#' @return List of dataframes of output from muLand program
#'
#' @author Manhan Group LLC
#' @export
returnMuLandOutputs <- function(inputList, workDir) {
  
  # set path to MuLand output directory
  outputDir <- file.path(workDir, "output")
  
  # ensure the MuLand output directory exists
  if(!dir.exists(outputDir)){
    dir.create(outputDir)
    #msg <- paste("Output directory does not exist and just created:",
    #             outputDir,
    #             sep = " ")
    
   # stop(msg)
  }
  
  # create data dictionary of the elements of the expected
  # return elements of the MuLand program
  muLandResultDict <- list(
    names = c("bh",
              "bids",
              "location",
              "location_probability",
              "rents"),
    cols = list(
      c("Agents",
        "Value"),
      c("Realestate",
        "Zone"),
      c("Realestate",
        "Zone"),
      c("Realestate",
        "Zone"),
      c("Realestate",
        "Zone",
        "Value"))
  )
  
  # initialize the return list of DataFrames
  outputList <- list()
  
  # for each specified DataFrame
  for(i in seq_along(muLandResultDict[["names"]])) {
    dfName <- muLandResultDict[["names"]][i]
    dfCols <- muLandResultDict[["cols"]][[i]]
    
    # if the MuLand output csv file exists
    fn <- file.path(outputDir, paste0(dfName, ".csv"))
    if(file.exists(fn)) {
      # load the MuLand output csv file into the return list 
      outputList[[dfName]] <- read.csv(file = fn, sep = ";")
      
      # check MuLand ouputs contains all columns specified
      if(any(!dfCols %in% names(outputList[[dfName]]))) {
        wrongCols <-
          dfCols[!dfCols %in% names(outputList[[dfName]])]
        
        msg <- paste0("Output '",
                      dfName,
                      "' does not contain specified columns: ",
                      paste(wrongCols, collapse = ", "))
        
        stop(msg)
      }
    } else {
      msg <- paste0("File does not exist: ", fn)
    }
  }
  
  # use the location shares output to ensure the location output is correct
  # muLand contains a bug that can write out incorrect location output
  # location = location shares * supply
  outputList[["location"]] <- merge(x = outputList[["location_probability"]],
                                    y = inputList[["supply"]],
                                    by.x = c("Realestate", "Zone"),
                                    by.y = c("V_IDX", "I_IDX"))
  
  loc_cols_cond <- !(colnames(outputList[["location"]]) %in% c("Realestate",
                                                               "Zone",
                                                               "NREST"))
  
  outputList[["location"]][, loc_cols_cond] <- 
    outputList[["location"]][, loc_cols_cond] * outputList[["location"]]$NREST
  
  outputList[["location"]] <- subset(outputList[["location"]],
                                     select = -c(NREST))
  
  write.table(x = outputList[["location"]],
              file = file.path(workDir, "output/location.csv"),
              sep = ";",
              row.names = FALSE,
              quote=FALSE)
  
  # return muLand outputs
  return(outputList)
  
}




# Run muLand -----------------------------------------------------------------
#' Read in outputs from the muLand program
#'
#' Runs the muLand program validating the inputs to the program and returning
#' the validated outputs. See the R functions checkMuLandInputs and 
#' returnMuLandOutputs for detailed documentation regarding data structures of
#' the muLand program inputs and outputs.
#' 
#'
#' @inheritParams checkMuLandInputs
#' @inheritParams returnMuLandOutputs
#' 
#' @param inputList List of data frames of input to muLand program
#' @param workDir String of target muLand working directory
#' @param createDir Logical (optional) indicator of whether to create the
#'   target muLand working directory if it does not exist, defaults to TRUE
#'
#' @return List of dataframes of output from muLand program
#'
#' @author Manhan Group LLC
#' @export
runMuLand <- function(inputList, workDir, createDir = TRUE) {
  
  # check that the inputs to the MuLand utility are valid
  if(checkMuLandInputs(inputList, workDir, createDir)){
    
    # for each input list of DataFrames write out a csv file
    # to the input working directory input sub-directory
    for(i in seq_along(inputList)){
      write.table(x = inputList[[i]],
                  file = file.path(workDir,
                                   "input",
                                   paste0(names(inputList[i]),
                                          ".csv")),
                  sep = ";",
                  row.names = FALSE,
                  quote=FALSE)
    }
    
    # run the MuLand utility
    system2(command = "../mu-land.exe",
            args = c(workDir), 
            stdout = file.path(workDir, paste(workDir, "log", sep = ".")),
            wait = TRUE)
    
    # return results from MuLand utility if valid
    results <- returnMuLandOutputs(inputList, workDir)
    
    return(results)
    
  } else {
    stop("Invalid input parameters specified to MuLand utility")
  }
  
}









# Run muLand until convergence -----------------------------------------------
#' Run muLand until convergence
#'
#' Runs the muLand program calling the runMuLand R function comparing total
#' number of units by agent type from the muLand program output to demand
#' control totals specified in the muLand program input. If convergence is not
#' achieved the input bid adjustments are altered so the calibration constants
#' better fit the input demand control totals. Additionally, the inputs are
#' further adjusted via an optional scenario-specific user-created endogenous
#' function. 
#' 
#' This function quits before convergence is reached if it has run the maximum
#' number of iterations specified or the percentage change in the convergence
#' criteria from iteration to iteration falls below a specified tolerance
#' parameter.
#' 
#' Convergence criteria is defined as the maximum percentage error of allocated
#' units to demand control totals across all agent types being less than the
#' specified tolerance parameter.
#' 
#'
#' @inheritParams runMuLand
#' @inheritParams nullEndogFn
#' 
#' @param inputList List of data frames of input to muLand program
#' @param workDir String of target muLand working directory
#' @param createDir Logical (optional) indicator of whether to create the
#'   target muLand working directory if it does not exist, defaults to TRUE
#' @param endogFn Function (optional) specifiying further transformations to
#'   be made to the inputList to better satisfy the convergence criteria, the
#'   default value is a NULL function that applies no transformations to the
#'   inputList
#' @param tol Numeric (optional) percentage defining the acceptable maximum
#'   percent error (APE) to consider a muLand run having reached convergence,
#'   default value is one percent
#' @param changeTol Numeric (optional) percentage defining the minimum
#'   percentage change of the maximum percentage error from iteration to
#'   iteration to allow the muLand program to continue iterating, default
#'   value is one percent
#' @param iterations Integer (optional) defining the maximum number of times
#'   to run the muLand program if convergence is not reached, default value
#'   is ten iterations
#'
#' @return List of dataframes of output from final muLand program run
#'   satisfying the convergence criteria or maximum number of iterations or
#'   minimum percentage change of maximum percentage error from iteration to
#'   iteration
#'
#' @author Manhan Group LLC
#' @export
fsRun <- function(inputList, workDir, createDir=TRUE, endogFn=nullEndogFn,
                  tol=1, changeTol = 1, iterations=10) {
  require(dplyr)
  # start_time <- Sys.time()
  # for each iteration
  for (i in 1:iterations) {
    
    # run the MuLand utility and return result set
    outputList <- runMuLand(inputList, workDir, createDir)
    
    # summarize the MuLand location output across all H_IDX values
    # and join with MuLand demand input and compute absolute percentage error
    # within each H_IDX of the output results to the input demand control total
    checkEqDemand <- reshape(data = outputList[["location"]],
                             varying = names(outputList[["location"]])[-1:-2],
                             v.names = "units",
                             timevar = "H_IDX",
                             idvar = "id",
                             direction = "long") %>%
      dplyr::group_by(H_IDX) %>%
      dplyr::summarise(NUNIT = sum(units)) %>%
      dplyr::left_join(y = inputList[["demand"]],
                       by = "H_IDX") %>%
      dplyr::mutate(err = abs(NUNIT - NAGENT))
    
    # compute the weighted average absolute percentage error (APE)
    WAAPE <- 100*sum(checkEqDemand$err)/sum(checkEqDemand$NAGENT)
    # the convergence measure used to be max. APE but that doesn't work great here
    
    # compute the percentage difference between current iterations APE
    # and the previous iteration (if no previous iteration set to the
    # changeTol parameter to ensure further execution)
    if(exists("last_WAAPE")){
      changePct <- 100 * abs(WAAPE/last_WAAPE - 1)
    } else {
      changePct <- changeTol
    }
    
    print(paste("Weighted average absolute percentage error:",
                paste0(round(WAAPE, 2), "%")))
    
    # if the maximum APE is less than the tolerance parameter
    # then the run has converged and the MuLand ouput list is returned
    if(WAAPE < tol) {
      print("Run converged, exiting...")
      break
    } else if (changePct < changeTol) {
    # if the run has not converged and the percent change of the previous
    # iterations maximum APE to the current iterations maximum APE is less
    # than the change tolerance parameter then stop iterating
    # the run has not converged and the MuLand output list is returned
      print("Supply and demand do not balance, exiting...")
      break
    } else {
    # if the run has not converged then
    # adjust the input calibration constants to
    # better fit the input demand control total
    # apply scenario-specific endogenous function
    # and move onto the next iteration
      last_WAAPE <- WAAPE
      
      outputList[["bh"]] <- outputList[["bh"]] %>%
        dplyr::left_join(y = checkEqDemand,
                         by = c("Agents" = "H_IDX")) %>%
        dplyr::transmute(Agents = Agents,
                         Value = log(NAGENT / NUNIT))
      
      write.table(x = outputList[["bh"]],
                  file = file.path(workDir, "output/bh.csv"),
                  sep = ";",
                  row.names = FALSE,
                  quote=FALSE)
      
      
      # calibrate and adjust bid adjustments in input
      inputList[["bids_adjustments"]] <- inputList[["bids_adjustments"]] %>%
        dplyr::left_join(y = outputList[["bh"]],
                         by = c("H_IDX" = "Agents")) %>%
        dplyr::transmute(H_IDX = H_IDX,
                         V_IDX = V_IDX,
                         I_IDX = I_IDX,
                         BIDADJ = BIDADJ + Value)
      
      # apply scenario-specific input list adjustments
      inputList <- endogFn(inputList, outputList)
    }
  }
  # end_time <- Sys.time()
  # dur = end_time - start_time
  # print(paste0("Run time: ",round(dur,2)," minutes"))
  
  return(outputList)
  
}
