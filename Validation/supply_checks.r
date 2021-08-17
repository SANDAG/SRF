library(dplyr)
library(reshape2)
## first, check overall regional totals
# read target data
library(readxl)
MGRA_target <- read_excel(file.path("target","mgra13_based_input2018.xlsx"), sheet=2)
target_total = array()
target_total[1] <- sum(MGRA_target$hs_sf)
target_total[2] <- sum(MGRA_target$hs_mf)
target_total[3] <- sum(MGRA_target$emp_total)
# compare with regional control total inputs to Supply
supply_totals_in <- read.csv(file.path("..","Supply","SR13_Regional_Totals_interpolated.csv"))
input_total = array()
input_total[1] <- supply_totals_in$hs_sf[supply_totals_in$year==2018]
input_total[2] <- supply_totals_in$hs_mf[supply_totals_in$year==2018]
input_total[3] <- supply_totals_in$ws_ind[supply_totals_in$year==2018] +
  supply_totals_in$ws_com[supply_totals_in$year==2018] +
  supply_totals_in$ws_ofc[supply_totals_in$year==2018]
# now compare with model output for 2018
processed_out <- read.csv(file.path("..","PostProcessor","Data","mgra13_based_input2018.csv"))
output_total = array()
output_total[1] <- sum(processed_out$hs_sf)
output_total[2] <- sum(processed_out$hs_mf)
output_total[3] <- sum(processed_out$emp_total)
compare_supply_totals <- data.frame(cbind(unit_type = c("hs_sf","hs_mf","emp"),
                                          target_total,input_total,output_total))
write.csv(compare_supply_totals,file.path("results","compare_supply_totals.csv"),row.names = FALSE)
## next, check distribution - by TAZ for a variety of reasons
# pull total area by real estate supply type by TAZ (summarized from parcel data using QGIS)
area_summary <- read.csv(file.path("target","area_summary.csv"))
# perform equivalent summary using output from the model for 2018
forecast_out <- read.csv(file.path("..","PostProcessor","Data","forecasted_year_2018.csv"))
forecast_sel <- left_join(select(forecast_out,MGRA,
                                 dev_sf,dev_mf,dev_mh,dev_indus,dev_comm,dev_office,dev_oth),
                          select(processed_out,mgra,taz),
                          by=c("MGRA"="mgra")) %>%
#  mutate(dev_res = dev_sf + dev_mf) %>%
  group_by(taz) %>%
  summarise(sfd_area = sum(dev_sf),
            mfd_area = sum(dev_mf),
            mhd_area = sum(dev_mh),
            ind_area = sum(dev_indus),
            com_area = sum(dev_comm),
            ofc_area = sum(dev_office),
            oth_area = sum(dev_oth))
a_totals = list()
a_totals$sfd = sum(forecast_sel$sfd_area)
a_totals$mfd = sum(forecast_sel$mfd_area)
a_totals$mhd = sum(forecast_sel$mhd_area)
a_totals$ind = sum(forecast_sel$ind_area)
a_totals$com = sum(forecast_sel$com_area)
a_totals$ofc = sum(forecast_sel$ofc_area)
a_totals$oth = sum(forecast_sel$oth_area)
forecast_sel$SingleFamily <- forecast_sel$sfd_area/a_totals$sfd
forecast_sel$MultiFamily <- forecast_sel$mfd_area/a_totals$mfd
forecast_sel$MobileHomes <- forecast_sel$mhd_area/a_totals$mhd
forecast_sel$Industrial <- forecast_sel$ind_area/a_totals$ind
forecast_sel$Commercial <- forecast_sel$com_area/a_totals$com
forecast_sel$Office <- forecast_sel$ofc_area/a_totals$ofc
forecast_sel$Other <- forecast_sel$oth_area/a_totals$oth
compare_area <- forecast_sel %>%
  melt(measure.vars = c(9:15),
       id.vars = c("taz")) %>%
  mutate(V_IDX = 1*(variable=="SingleFamily")+
           2*(variable=="MultiFamily")+
           3*(variable=="MobileHomes")+
           4*(variable=="Industrial")+
           5*(variable=="Commercial")+
           6*(variable=="Office")+
           7*(variable=="Other")) %>%
  left_join(area_summary,
            by=c("taz"="TAZ","V_IDX"="V_IDX")) %>%
  mutate(share = ifelse(is.na(share)==TRUE,0,share)) %>%
  filter(V_IDX > 0) %>%
  group_by(taz,V_IDX) %>%
  summarise(est_share = sum(value), obs_share = sum(share))
#compare_area[is.na(compare_area)] <- 0
compare_area$abs_err <- abs(compare_area$obs_share - compare_area$est_share)
supply_WAAPEs = group_by(compare_area,V_IDX) %>%
  summarise(WAAPE = sum(abs_err))
write.csv(supply_WAAPEs,file.path("results","supply_WAAPEs.csv"),row.names = FALSE)
