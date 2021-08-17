# read target data
library(readxl)
MGRA_target <- read_excel(file.path("target","mgra13_based_input2018.xlsx"), sheet=2)
# now compare with model output for 2018
processed_out <- read.csv(file.path("..","PostProcessor","Data","mgra13_based_input2018.csv"))
library(dplyr)
MGRA_comparison <- inner_join(MGRA_target,
                              processed_out,
                              by=c("mgra"="mgra","taz"="taz","zip09"="zip09","luz_id"="luz_id"),
                              suffix=c(".obs",".est"))
MGRA_comparison$hh.err = MGRA_comparison$hh.est - MGRA_comparison$hh.obs
MGRA_comparison$emp.err = MGRA_comparison$emp_total.est - MGRA_comparison$emp_total.obs
hh_WAAPE_mgra = sum(abs(MGRA_comparison$hh.err))/sum(MGRA_comparison$hh.obs)
emp_WAAPE_mgra = sum(abs(MGRA_comparison$emp.err))/sum(MGRA_comparison$emp_total.obs)
write.csv(MGRA_comparison,file.path("results","MGRA_comparison.csv"),row.names = FALSE)
TAZ_comparison <- MGRA_comparison %>%
  group_by(taz) %>%
  summarise(hh.est = sum(hh.est),
            hh.obs = sum(hh.obs),
            hh.err = sum(hh.err),
            emp.est = sum(emp_total.est),
            emp.obs = sum(emp_total.obs),
            emp.err = sum(emp.err))
write.csv(TAZ_comparison,file.path("results","TAZ_comparison.csv"),row.names = FALSE)
hh_WAAPE_TAZ = sum(abs(TAZ_comparison$hh.err))/sum(TAZ_comparison$hh.obs)
emp_WAAPE_TAZ = sum(abs(TAZ_comparison$emp.err))/sum(TAZ_comparison$emp.obs)
