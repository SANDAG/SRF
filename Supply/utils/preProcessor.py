import os,sys,csv

totalsPath = sys.argv[1]
selectedYear = sys.argv[2]
paramsPathIn = sys.argv[3]
paramsPathOut = sys.argv[4]

keyDict = {}
prevYear = str(int(selectedYear) - 1)
with open(totalsPath, "r") as totalsFile:
    totalsReader = csv.reader(totalsFile)
    header = next(totalsReader)
    for row in totalsReader:
        if row[0]==prevYear:
            prev_hs_sf = float(row[1])
            prev_hs_mf = float(row[2])
            prev_ws_ind = float(row[3])
            prev_ws_com = float(row[4])
            prev_ws_ofc = float(row[5])
        if row[0] == selectedYear:
            keyDict['sf_growth'] = float(row[1]) - prev_hs_sf
            keyDict['mf_growth'] = float(row[2]) - prev_hs_mf
            keyDict['ind_growth'] = float(row[3]) - prev_ws_ind
            keyDict['com_growth'] = float(row[4]) - prev_ws_com
            keyDict['ofc_growth'] = float(row[5]) - prev_ws_ofc
output = open(paramsPathOut, "w")
with open(paramsPathIn, "r") as template:
    for line in template:
        outLine = line.format(**keyDict)
        output.write(outLine)
output.close()
