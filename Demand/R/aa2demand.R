library(dplyr)
library(reshape2)
library(mipfp)
args <- commandArgs(trailingOnly = TRUE)

ActivityLocations <- read.csv(args[1], stringsAsFactors = FALSE)
## NOTE: argument above needs to point to ActivityLocations.csv in AA output directory
hh_aa2demand_base <- read.csv(args[2], stringsAsFactors = FALSE) # e.g. "../hh_aa2demand_base.csv"
regional_totals <- read.csv(args[3], stringsAsFactors = FALSE) # e.g. "../SR13_Regional_Totals_interpolated.csv"
AA_Demand_Emp_Key <- read.csv(args[4], stringsAsFactors = FALSE) # e.g. "../AA_Demand_Emp_Key.csv"

year_index = 1 #could calculate instead with actual year - base year...
aa_hh_activity_names <- c("Households less than 25k annual income and 2 or less people",
                          "Households less than 25k annual income and 3 or more people",
                          "Households 25 to 150k annual income and 2 or less people",
                          "Households 25 to 150k annual income and 3 or more people",
                          "Households 150k or more annual income and 2 or less people",
                          "Households 150k or more annual income and 3 or more people")

aa_cat_margin <- filter(ActivityLocations,
                        Activity %in% aa_hh_activity_names,
                        ZoneNumber %in% 1:229) %>%
  mutate(aa_hh_cat = match(Activity,aa_hh_activity_names)) %>%
  select(LUZ=ZoneNumber,aa_hh_cat,Quantity) %>%
  arrange(LUZ,aa_hh_cat)
abm_inc_margin <- regional_totals[43:52,year_index + 1]
ipf_result <- Ipfp(seed=as.matrix(hh_aa2demand_base[,4:13]),
                   target.list = c(1,2),
                   target.data = c(as.array(aa_cat_margin$Quantity),
                                   abm_inc_margin),
                   print = TRUE)
hh_4demand <- cbind(select(hh_aa2demand_base,LUZ,aa_inc_cat,aa_siz_cat),
                    t(t(10*ipf_result$p.hat)*abm_inc_margin)) %>%
  melt(measure.vars = 4:13,value.name = "hh",variable.name="abm_inc_cat") %>%
  mutate(demand_inc_cat = as.integer(abm_inc_cat),
         IDAGENT = (demand_inc_cat - 1)*2 + aa_siz_cat) %>%
  group_by(LUZ,IDAGENT) %>%
  summarise(NAGENT = sum(hh))
jobs_4demand <- left_join(ActivityLocations,AA_Demand_Emp_Key,
                          by=c("Activity"="Activity")) %>%
  filter(is.na(Demand_ID)==FALSE) %>%
  select(LUZ=ZoneNumber,IDAGENT=Demand_ID,Quantity) %>%
  group_by(LUZ,IDAGENT) %>%
  summarise(NAGENT=sum(Quantity))
demand_input <- rbind(as.data.frame(hh_4demand),as.data.frame(jobs_4demand)) %>%
  filter(LUZ<=229) %>%
  arrange(LUZ,IDAGENT)

write.csv(demand_input,paste0("master_demand_year",year_index,".csv"),row.names = FALSE)
