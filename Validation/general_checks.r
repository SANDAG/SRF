# read target data
library(readxl)
MGRA_target <- read_excel(file.path("target","mgra13_based_input2018.xlsx"), sheet=2)
# now compare with model output for 2018
processed_out <- read.csv(file.path("..","PostProcessor","Data","mgra13_based_input2018.csv"))
library(dplyr)
MGRA_comparison <- inner_join(MGRA_target,
                              processed_out,
                              by=c("mgra"="mgra"),
                              suffix=c(".obs",".est"))
MGRA_comparison$hh.err = MGRA_comparison$hh.est - MGRA_comparison$hh.obs
MGRA_comparison$emp.err = MGRA_comparison$emp_total.est - MGRA_comparison$emp_total.obs
hh_WAAPE = sum(abs(MGRA_comparison$hh.err))/sum(MGRA_comparison$hh.obs)
emp_WAAPE = sum(abs(MGRA_comparison$emp.err))/sum(MGRA_comparison$emp_total.obs)
write.csv(MGRA_comparison,file.path("results","MGRA_comparison.csv"),row.names = FALSE)
