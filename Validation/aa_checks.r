library(dplyr)
library(reshape2)
# this is redundant if you ran "supply_checks.r" first
library(readxl)
MGRA_target <- read_excel(file.path("target","mgra13_based_input2018.xlsx"), sheet=2)
## first check the control totals
# targets:
obs_hh_inc_sums <- colSums(MGRA_target[13:22])
obs_Rtotal_jobs <- colSums(MGRA_target[26:55])
# output (redundant if you ran "supply_checks.r" first):
processed_out <- read.csv(file.path("..","PostProcessor","Data","mgra13_based_input2018.csv"))
est_hh_inc_sums <- colSums(processed_out[13:22])
est_Rtotal_jobs <- colSums(processed_out[26:55])
compare_res_totals <- as.data.frame(cbind(obs_hh_inc_sums,est_hh_inc_sums))
compare_res_totals$err = compare_res_totals$obs_hh_inc_sums - compare_res_totals$est_hh_inc_sums
res_total_WAAPE = sum(abs(compare_res_totals$err))/sum(compare_res_totals$obs_hh_inc_sums)
compare_job_totals <- as.data.frame(cbind(obs_Rtotal_jobs,est_Rtotal_jobs))
compare_job_totals$err = compare_job_totals$obs_Rtotal_jobs - compare_job_totals$est_Rtotal_jobs
job_total_WAAPE = sum(abs(compare_job_totals$err))/sum(compare_job_totals$obs_Rtotal_jobs)
write.csv(compare_res_totals,file.path("results","compare_res_totals.csv"),row.names = FALSE)
write.csv(compare_job_totals,file.path("results","compare_job_totals.csv"),row.names = FALSE)
## now check distribution by LUZ
hh_activity_LUZ <- left_join(cbind(select(MGRA_target,mgra),MGRA_target[13:22]) %>%
                               melt(measure.vars = 2:11) %>%
                               left_join(select(forecast_out,MGRA,LUZ), by=c("mgra"="MGRA")) %>%
                               dcast(LUZ ~ variable, fun.aggregate = sum),
                             cbind(select(processed_out,mgra),processed_out[13:22]) %>%
                               melt(measure.vars = 2:11) %>%
                               left_join(select(forecast_out,MGRA,LUZ), by=c("mgra"="MGRA")) %>%
                               dcast(LUZ ~ variable, fun.aggregate = sum),
                             by=c("LUZ"="LUZ"), suffix=c(".obs",".est"))
hh_WAAPEs = list()
for (ix in 1:10) {
  # convert to shares first (isolate the allocation portion of process from total differences)
  estvarname = paste(paste0("i",ix),"est",sep = ".")
  estvar_sum = sum(hh_activity_LUZ[[estvarname]])
  hh_activity_LUZ[[estvarname]] = hh_activity_LUZ[[estvarname]]/estvar_sum
  obsvarname = paste(paste0("i",ix),"obs",sep = ".")
  obsvar_sum = sum(hh_activity_LUZ[[obsvarname]])
  hh_activity_LUZ[[obsvarname]] = hh_activity_LUZ[[obsvarname]]/obsvar_sum
  # now compute errors and WAAPEs
  errvarname = paste(paste0("i",ix),"err",sep = ".")
  hh_activity_LUZ[[errvarname]] = hh_activity_LUZ[[estvarname]] - hh_activity_LUZ[[obsvarname]]
  hh_WAAPEs[paste0("i",ix)] = sum(abs(hh_activity_LUZ[[errvarname]]))/sum(hh_activity_LUZ[[obsvarname]])
}
write.csv(hh_WAAPEs,file.path("results","hh_WAAPEs.csv"),row.names = FALSE)
job_activity_LUZ <- left_join(cbind(select(MGRA_target,mgra),MGRA_target[26:55]) %>%
                                melt(measure.vars = 2:31) %>%
                                left_join(select(forecast_out,MGRA,LUZ), by=c("mgra"="MGRA")) %>%
                                dcast(LUZ ~ variable, fun.aggregate = sum),
                              cbind(select(processed_out,mgra),processed_out[26:55]) %>%
                                melt(measure.vars = 2:31) %>%
                                left_join(select(forecast_out,MGRA,LUZ), by=c("mgra"="MGRA")) %>%
                                dcast(LUZ ~ variable, fun.aggregate = sum),
                              by=c("LUZ"="LUZ"), suffix=c(".obs",".est"))
job_activity_names <- colnames(MGRA_target[26:55])
job_WAAPEs = list()
for (varname in job_activity_names) {
  # convert to shares first (isolate the allocation portion of process from total differences)
  estvarname = paste(varname,"est",sep = ".")
  estvar_sum = sum(job_activity_LUZ[[estvarname]])
  job_activity_LUZ[[estvarname]] = job_activity_LUZ[[estvarname]]/estvar_sum
  obsvarname = paste(varname,"obs",sep = ".")
  obsvar_sum = sum(job_activity_LUZ[[obsvarname]])
  job_activity_LUZ[[obsvarname]] = job_activity_LUZ[[obsvarname]]/obsvar_sum
  # now compute errors and WAAPEs
  errvarname = paste(varname,"err",sep = ".")
  job_activity_LUZ[[errvarname]] = job_activity_LUZ[[estvarname]] - job_activity_LUZ[[obsvarname]]
  job_WAAPEs[varname] = sum(abs(job_activity_LUZ[[errvarname]]))/sum(job_activity_LUZ[[obsvarname]])
}
write.csv(job_WAAPEs,file.path("results","job_WAAPEs.csv"),row.names = FALSE)
