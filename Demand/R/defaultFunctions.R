# Null access function --------------------------------------------------
#' Null access function
#'
#' Default null access function used as default placeholder for 
#' model-specific user created access function. Used to calculate
#' user-defined access to/from input scenario zones.
#' 
#'
#' @param inputList List of data frames of input to muLand program
#' @param outputList List of dataframes of output from muLand program
#' @param skims User-defined skim matrices defining zonal accessibilites
#'
#' @return Dataframe of zones from input list to muLand program with
#'   user-defined accessibility calculations
#'
#' @author Manhan Group LLC
#' @export 
nullAccessFn <- function(inputList, outputList, skims) {
  
  return(inputList[["zones"]])
  
}

# Null endogenous function --------------------------------------------------
#' Null endogenous function
#'
#' Default null endogenous function used as default placeholder for 
#' model-specific user created endogenous function to use in fsRun R function
#' that modifies input data to muLand program if the program does not converge.
#' 
#'
#' @param inputList List of data frames of input to muLand program
#' @param outputList List of dataframes of output from muLand program
#'
#' @return Unaltered inputList parameter
#'
#' @author Manhan Group LLC
#' @export 
nullEndogFn <- function(inputList, outputList){
  
  return(inputList)
  
}




# Null stop function ---------------------------------------------------------
#' Null stop function
#'
#' Default null stop function used as default placeholder for 
#' model-specific user created stop function. Used to calculate
#' user-defined stopping criteria based on inputs and outputs to the
#' muLand program.
#' 
#'
#' @param inputList List of data frames of input to muLand program
#' @param outputList List of dataframes of output from muLand program
#'
#' @return Logical indicator if stopping criteria satisfied
#'
#' @author Manhan Group LLC
#' @export 
nullStopFn <- function(inputList, outputList) {
  
  return(TRUE)
  
}
