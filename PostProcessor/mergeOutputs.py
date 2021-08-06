import os, sys, csv, math

year = sys.argv[1]

oldMGRAs = os.path.join("Data","mgra13_based_input"+str(int(year)-1)+".csv")
Dsummary = os.path.join("..","Demand",year,"combined_summary.csv")
supplyIO = os.path.join("Data","forecasted_year_"+year+'.csv')
newMGRAs = os.path.join("Data","mgra13_based_input"+year+".csv")

hhFields2copy = ['hh','hh_sf','hh_mf','hh_mh','hhp',
'i1','i2','i3','i4','i5','i6','i7','i8','i9','i10']
empFields2copy = ['emp_ag',
'emp_const_non_bldg_prod',
'emp_const_non_bldg_office',
'emp_utilities_prod',
'emp_utilities_office',
'emp_const_bldg_prod',
'emp_const_bldg_office',
'emp_mfg_prod',
'emp_mfg_office',
'emp_whsle_whs',
'emp_trans',
'emp_retail',
'emp_prof_bus_svcs',
'emp_prof_bus_svcs_bldg_maint',
'emp_pvt_ed_k12',
'emp_pvt_ed_post_k12_oth',
'emp_health',
'emp_personal_svcs_office',
'emp_amusement',
'emp_hotel',
'emp_restaurant_bar',
'emp_personal_svcs_retail',
'emp_religious',
'emp_pvt_hh',
'emp_state_local_gov_ent',
'emp_fed_non_mil',
'emp_fed_mil',
'emp_state_local_gov_blue',
'emp_state_local_gov_white',
'emp_public_ed']

demand_data = {}
with open(Dsummary, 'r') as demand_summary:
    summary_reader = csv.DictReader(demand_summary)
    for row in summary_reader:
        demand_data[int(row['Zone'])] = row

supply_data = {}
with open(supplyIO, 'r') as supply_output:
    supply_reader = csv.DictReader(supply_output)
    for row in supply_reader:
        supply_data[int(row['MGRA'])] = row

MGRA_output = open(newMGRAs, 'w', newline='')
with open(oldMGRAs, 'r') as MGRA_template:
    mgra_reader = csv.DictReader(MGRA_template)
    MGRA_writer = csv.DictWriter(MGRA_output,mgra_reader.fieldnames)
    MGRA_writer.writeheader()
    for row in mgra_reader:
        MGRA = int(row['mgra'])
        acres = float(row['acres'])
        demand_row = demand_data[MGRA]
        supply_row = supply_data[MGRA]
        if (float(row['hs'])>0):
            hs_growth = float(supply_row['hs']) / float(row['hs'])
            row['duden'] = hs_growth * float(row['duden'])
        else:
            row['duden'] = float(supply_row['hs']) / acres
        row['hs'] = supply_row['hs']
        row['hs_sf'] = supply_row['hs_sf']
        row['hs_mf'] = supply_row['hs_mf']
        row['hs_mh'] = supply_row['hs_mh']
        emp_total = 0
        emp_prior = float(row['emp_total'])
        emp_retail_prior = float(row['emp_retail'])
        for field in empFields2copy:
            if (demand_row[field]!='NA'):
                row[field] = demand_row[field]
                emp_total = emp_total + float(demand_row[field])
        row['emp_total'] = emp_total
        if (emp_prior>0):
            emp_growth = emp_total / emp_prior
            row['empden'] = emp_growth * float(row['empden'])
        else:
            row['empden'] = emp_total / acres
        if (emp_retail_prior > 0):
            emp_retail_growth = float(row['emp_retail'])/emp_retail_prior
            row['retempden'] = emp_retail_growth * float(row['retempden'])
        else:
            row['retempden'] = float(row['emp_retail']) / acres
        if (float(row['hh']) > 0 and float(row['hhp']) > 0):
            row['hhs'] = float(row['hhp']) / float(row['hh'])
        # don't do anything to average household size if either of those are 0
        pop_prior = float(row['pop'])
        if (demand_row['hhp']!='NA'):
            row['pop'] = float(demand_row['hhp']) + float(row['gq_civ']) + float(row['gq_mil'])
        if (pop_prior>0):
            pop_growth = float(row['pop']) / pop_prior
            row['popden'] = pop_growth * float(row['popden'])
        else:
            row['popden'] = float(row['pop']) / acres
        MGRA_writer.writerow(row)

MGRA_output.close()
