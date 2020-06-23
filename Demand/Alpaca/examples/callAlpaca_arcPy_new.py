## Test script to call "Alpaca" web service (for MAPC Community Viz case study)
## by: Colby M Brown, AICP PTP
## Principal and Founder, Manhan Group LLC
## e-mail: colby@manhangroup.com
#standard library imports
import sys, os, json, csv
#libraries for web service request
import requests
#ArcGIS
import arcpy
arcpy.env.overwriteOutput = True
#input file geodatabase
# ws = arcpy.GetParameterAsText(0)# r'E:\Manhan_Group\LincolnInstitute\MAPC\placeout_analysis_09_16_2015_2\placeout_analysis\CVAnalysis.gdb'  
# input parcels
parcel = arcpy.GetParameterAsText(0) # r'E:\Manhan_Group\LincolnInstitute\MAPC\placeout_analysis_09_16_2015_2\placeout_analysis\CVAnalysis.gdb\Parcels_L3E' 
pTypes = arcpy.GetParameterAsText(1) # r'E:\Manhan_Group\LincolnInstitute\MAPC\placeout_analysis_09_16_2015_2\placeout_analysis\CVAnalysis.gdb\PLACE_TYPES'
bTypes = arcpy.GetParameterAsText(2) # r'E:\Manhan_Group\LincolnInstitute\MAPC\placeout_analysis_09_16_2015_2\placeout_analysis\CVAnalysis.gdb\bType_table'
# added support for building points
bPoint = arcpy.GetParameterAsText(3) # r'E:\Manhan_Group\LincolnInstitute\MAPC\placeout_analysis_09_16_2015_2\placeout_analysis\CVAnalysis.gdb\WorkshopLyrs\BuildingTypes'
# agent attributes table (to use these in conjunction with location probability data)
agents = arcpy.GetParameterAsText(4) # r'E:\Manhan_Group\LincolnInstitute\MAPC\boston-csv\agents.csv' 
#intermediate files & logs
out_json = r'E:\Manhan_Group\LincolnInstitute\MAPC\test.json' # arcpy.GetParameterAsText
#output data
outShapefile = arcpy.GetParameterAsText(5) # r'E:\Manhan_Group\LincolnInstitute\MAPC\test.shp'

arcpy.AddMessage("Reading input data...")

agentDict = {}
with open(agents, 'rb') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	for row in reader:
		agentDict[row['IDAGENT']] = row # the whole dict

bTypes_idx = {}
bType_fields = ["LU_Dwelling_Unit_Count","LU_Dwelling_Unit_Density","DU_Size","LU_A_Bedrooms_Count","Style_Name"]
with arcpy.da.SearchCursor(bTypes, bType_fields) as cursor: 
	for row in cursor:
		bType_attr = {}
		bType_attr['LU_Dwelling_Unit_Count'] = row[0]
		bType_attr['LU_Dwelling_Unit_Density'] = row[1]
		bType_attr['DU_Size'] = row[2]
		bType_attr['LU_A_Bedrooms_Count'] = row[3]
		bType_id = row[4]
		bTypes_idx[bType_id] =  bType_attr

pTypes_idx = {}
pType_fields = ["BLTYPE1","BLTYPE2","BLTYPE3","BLTYPE4","BLTYPE5","BLTYPE6","BLTYPE7","BLTYPE8","BLTYPE9","BLTYPE10","BLTYPE1_SHARE","BLTYPE2_SHARE","BLTYPE3_SHARE","BLTYPE4_SHARE","BLTYPE5_SHARE","BLTYPE6_SHARE","BLTYPE7_SHARE","BLTYPE8_SHARE","BLTYPE9_SHARE","BLTYPE10_SHARE","PTYPE_INIT"]
with arcpy.da.SearchCursor(pTypes, pType_fields) as cursor:
	for row in cursor:
		bType_list = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]]
		share_list = [row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19]]
		pType_id = row[20]
		pTypes_idx[pType_id] = (bType_list, share_list)
	
# input SpatialReference
# NAD_1983_StatePlane_Massachusetts_Mainland_FIPS_2001
# inSpatialRef = arcpy.SpatialReference(26986)
# output SpatialReference
# GCS_WGS_1984
outSpatialRef = arcpy.SpatialReference(4326)
# create the CoordinateTransformation
parcel_lyr = os.path.join(arcpy.env.scratchGDB, "Parcels_WM")
arcpy.Project_management(parcel, parcel_lyr, outSpatialRef, "WGS_1984_(ITRF00)_To_NAD_1983")
bPoint_lyr = os.path.join(arcpy.env.scratchGDB, "bPoints_WM")
arcpy.Project_management(bPoint, bPoint_lyr, outSpatialRef, "WGS_1984_(ITRF00)_To_NAD_1983")

# finally, iterate through the parcels and generate the supply inventory
loclist = [] # a list of point locations (parcels)
zones = [] # a separate list -- to keep track of IDs

parcel_fields = ["SHAPE@XY","Allocated_Dev_DU","place_type","mapc_id","Net_Additional_Comm_Floor_Area_Final_Estimate2","building_types_count"]
with arcpy.da.SearchCursor(parcel_lyr, parcel_fields) as cursor:
	for row in cursor:
		# get dwelling units
		totalDU = row[1]
		if totalDU == 0:
			continue
		#also check whether there are any building points overriding the place type
		bPoints_cnt = row[5]
		if bPoints_cnt > 0:
			continue
		loc = {}
		parType = row[2]
		if not(parType in pTypes_idx):
			continue
		# get centroid X, Y
		lon = row[0][0]
		lat = row[0][1]
		coords = [lon, lat]
		loc['lnglat'] = coords
		# get MAPC ID - for joining results back up later
		mapc_id = row[3]
		comm_sf = row[4]
		pType_info = pTypes_idx[parType]
		bType_list = pType_info[0]
		share_list = pType_info[1]
		units = [0]*5
		for bt in range(0, 9):
			if share_list[bt] > 0:
				bType = bType_list[bt]
				if not(bType in bTypes_idx):
					continue
				btype_unit = totalDU * share_list[bt]
				bType_attr = bTypes_idx[bType]
				du = bType_attr['LU_Dwelling_Unit_Count']
				if du > 0:
					if comm_sf > 0:
						units[4] += btype_unit
					elif du == 1: # single-family
						units[0] += btype_unit
					elif du < 4: # duplex/triplex
						units[1] += btype_unit
					elif du < 10: # small apartment
						units[2] += btype_unit
					else:
						units[3] += btype_unit
		# at this point we should have a count of units by type.
		loc['units'] = []
		for re in range(0, 4):
			if units[re] > 0:
				unit = {}
				unit['type'] = re + 1
				unit['nrest'] = units[re]
				loc['units'].append(unit)
		if len(loc['units']) > 0:
			loclist.append(loc)
			zones.append({'coords': coords, 'id': mapc_id, 'units': units, 'income': [0]*5, 'hhsiz': [0]*5, 'head_age': [0]*5})
#now loop through the building points and append these as well.
bPoint_fields = ["SHAPE@XY","LU_Dwelling_Unit_Count","btype_name","ParcelID"]
with arcpy.da.SearchCursor(bPoint_lyr, bPoint_fields) as cursor:
	for row in cursor:
		# get dwelling units
		totalDU = row[1]
		if totalDU == 0:
			continue
		loc = {}
		bType = row[2]
		if not(bType in bTypes_idx):
			continue
		# get MAPC ID - for joining results back up later
		mapc_id = row[3]
		btype_unit = totalDU # not split into shares for placed buildings
		bType_attr = bTypes_idx[bType]
		du = bType_attr['LU_Dwelling_Unit_Count']
		if du > 0:
			if comm_sf > 0:
				units[4] += btype_unit
			elif du == 1: # single-family
				units[0] += btype_unit
			elif du < 4: # duplex/triplex
				units[1] += btype_unit
			elif du < 10: # small apartment
				units[2] += btype_unit
			else:
				units[3] += btype_unit
		# at this point we should have a count of units by type.
		loc['units'] = []
		for re in range(0, 4):
			if units[re] > 0:
				unit = {}
				unit['type'] = re + 1
				unit['nrest'] = units[re]
				loc['units'].append(unit)
		if len(loc['units']) > 0:
			loclist.append(loc)
			zones.append({'coords': coords, 'id': mapc_id, 'units': units, 'income': [0]*5, 'hhsiz': [0]*5, 'head_age': [0]*5})
		
# package up json call
call = {}
call['loc'] = loclist
# dump to disk - for debug only
call_json = open(out_json, 'wb')
json.dump(call, call_json)
call_json.close()

arcpy.AddMessage("Calling Alpaca web service...")
mulandweb_url = 'http://162.243.43.187:8000/boston'

headers = {'Content-Type': 'application/json'}
response = requests.post(mulandweb_url, data=json.dumps(call), headers=headers)
resp_data = response.json()
# print('Keys in response: ', list(resp_data.keys()))
if not('location_probability' in resp_data.keys()):
	arcpy.AddError(",".join(response.status_code,response.reason))
	raise arcpy.ExecuteError
arcpy.AddMessage("Extracting response...")

probs = resp_data['location_probability']
for row in probs:
	v = int(row[0])
	i = int(row[1])
	shares = row[2:]
	inc = 0
	siz = 0
	age = 0
	for h in range(1, 13):
		inc += shares[h-1]*agentDict[h]['INCOME']
		siz += shares[h-1]*agentDict[h]['HHSIZ']
		age += shares[h-1]*agentDict[h]['HEAD_AGE']
	zones[i-1]['income'][v-1] = inc
	zones[i-1]['hhsiz'][v-1] = siz
	zones[i-1]['head_age'][v-1] = age
# Create the output Layer
out_ws = os.path.dirname(outShapefile)
out_fn = os.path.basename(outShapefile)
arcpy.CreateFeatureclass_management(out_ws, out_fn, 'POINT', spatial_reference=outSpatialRef)
# Create the output shapefile
arcpy.AddField_management(outShapefile, "mapc_id", "LONG")
arcpy.AddField_management(outShapefile, "low_inc", "DOUBLE")
arcpy.AddField_management(outShapefile, "HoH_age", "DOUBLE")
arcpy.AddField_management(outShapefile, "HH_size", "DOUBLE")
c = arcpy.da.InsertCursor(outShapefile, ["SHAPE@","mapc_id","low_inc","HoH_age","HH_size"])
for zone in zones:
	wtd_inc = 0
	wtd_siz = 0
	wtd_age = 0
	unitsum = 0
	for v in range(0, 4):
		wtd_inc += zone['units'][v] * zone['income'][v]
		wtd_siz += zone['units'][v] * zone['hhsiz'][v]
		wtd_age += zone['units'][v] * zone['head_age'][v]
		unitsum += zone['units'][v]
	if unitsum > 0:
		avg_inc = wtd_inc / unitsum
		avg_siz = wtd_siz / unitsum
		avg_age = wtd_age / unitsum
	else: # not sure why this would happen
		continue # but just move on to the next one if it does
	# create the feature
	c.insertRow((arcpy.Point(zone['coords'][0],zone['coords'][1]), zone['id'], avg_inc, avg_age, avg_siz))
del c