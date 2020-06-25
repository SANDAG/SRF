## Test script to compute housing affordability metrics (with FresnoCOG Envision Tomorrow case study)
## by: Colby M Brown, AICP PTP
## Principal and Founder, Manhan Group LLC
## e-mail: colby@manhangroup.com

import csv, sys, os

rent_file = r'outputs\rents.csv'
locations = r'outputs\location_probability.csv'
in_supply = r'inputs\supply.csv'
hh_income = r'..\..\household_attrs_xtype_h1_winc.csv'
zoneNames = r'..\..\ZONE_NAMES.csv'

csvoutput = r'hai.csv'

rent = {}
with open(rent_file, 'rb') as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
    for row in csv_reader:
        v = int(row['Realestate'])
        i = int(row['Zone'])
        rent[(v,i)] = float(row['Value'])

supply = {}
with open(in_supply, 'rb') as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
    for row in csv_reader:
        v = int(row['V_IDX'])
        i = int(row['I_IDX'])
        supply[(v,i)] = float(row['NREST'])

avginc = {}
with open(hh_income, 'rb') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        h = int(row['HHTYPE'])
        avginc[h] = float(row['AVG_INCOME'])

zone_ix = {}
with open(zoneNames, 'rb') as lookup_file:
    ix_reader = csv.DictReader(lookup_file)
    for taz in ix_reader:
        zone_ix[int(taz['IDZONE'])] = int(taz['DESCZONE'])

zone_hh30 = {} # zonal households with burden > 30%
zone_hh50 = {} # zonal households with burden > 50%
zone_sfcb = {} # average housing cost burden (single family)
zone_mfcb = {} # average housing cost burden (multi-family)
with open(locations, 'rb') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        v = int(row[0])
        i = int(row[1])
        p = int(row[2:])
        if v in range(1, 3):
            wtd_hcb = 0
            for h in range(1, 26):
                hcb = (rent[(v, i)] * 12)  / avginc[h]
                hh = p[h-1] * supply[(v, i)]
                if hcb > 0.3:
                    zone_hh30[i] += hh
                elif hcb > 0.5:
                    zone_hh50[i] += hh
                wtd_hcb += p[h-1] * hcb
            if v == 1: #single-family
                zone_sfcb[i] = wtd_hcb
            elif v ==2: #multi-family
                zone_mfcb[i] = wtd_hcb
            
with open(csvoutput, 'wb') as out_file:
    csv_writer = csv.writer(out_file)
    csv_writer.writerow(['TAZ_MIP','SF','MF','DU','SFCB','MFCB','DUCB','SHR30','SHR50'])
    for i in sorted(zone_hh30.keys()):
        TAZ_MIP = zone_ix[i]
        SF = supply[(1, i)]
        MF = supply[(2, i)]
        DU = SF + MF
        SFCB = zone_sfcb[i]
        MFCB = zone_mfcb[i]
        DUCB = (SF * zone_sfcb[i] + MF * zone_mfcb[i])/DU
        SHR30 = zone_hh30[i] / DU
        SHR50 = zone_hh50[i] / DU
        csv_writer.writerow([TAZ_MIP,SF,MF,DU,SFCB,MFCB,DUCB,SHR30,SHR50])
    
