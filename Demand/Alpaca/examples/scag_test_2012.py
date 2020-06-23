## Test script to run mu-Land (with SCAG Urban Footprint case study)
## by: Colby M Brown, AICP PTP
## Principal and Founder, Manhan Group LLC
## e-mail: colby@manhangroup.com

#standard library imports
import sys, os, csv
import subprocess, shutil
#libraries for web service request
# import json, requests
#OGR bindings
from osgeo import ogr
# use OGR specific exceptions
ogr.UseExceptions()
#input file geodatabase
ws = 'SCAG_SCS_Scenarios_updated.gdb'
spz = 'SCAG_2012_base_canvas'
#input model zone system
luz = 'luz.shp'
#input template model structure - load into dictionaries
model_dir = 'scag-csv'
zones_csv = os.path.join(model_dir, 'zones.csv')
zonesDict = {}
with open(zones_csv, 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	zones_header = reader.next()
	for row in reader:
		zonesDict[row[0]] = row[1:]
realestate = os.path.join(model_dir, 'real_estates_zones.csv')
reDict = {}
with open(realestate, 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	re_header = reader.next()
	for row in reader:
		reDict[(row[0],row[1])] = row[2:]
access_att = os.path.join(model_dir, 'agents_zones.csv')
accattDict = {}
with open(access_att, 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	accatt_header = reader.next()
	for row in reader:
		accattDict[(row[0],row[1])] = row[2:]
agents = os.path.join(model_dir, 'agents.csv')
agentDict = {}
with open(agents, 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	reader.next()
	for row in reader:
		agentDict[row[0]] = row[1] # for this one we only care about market by agent
		
# get the driver
driver = ogr.GetDriverByName("OpenFileGDB")
# opening the FileGDB
try:
    gdb = driver.Open(ws, 0)
except Exception, e:
    print e
    sys.exit()
spz_lyr = gdb.GetLayer(spz)

# Create the output Layer
tmpDriver = ogr.GetDriverByName("MEMORY")

# Create the output shapefile
tmpDataSource = tmpDriver.CreateDataSource('centroids')
tmp=tmpDriver.Open('centroids',1)
tmpLayer = tmpDataSource.CreateLayer("spz_centroids", geom_type=ogr.wkbPoint)

# Add input Layer Fields to the output Layer
inLayerDefn = spz_lyr.GetLayerDefn()
for i in range(0, inLayerDefn.GetFieldCount()):
    fieldDefn = inLayerDefn.GetFieldDefn(i)
    tmpLayer.CreateField(fieldDefn)

# Get the output Layer's Feature Definition
tmpLayerDefn = tmpLayer.GetLayerDefn()

# Add features to the ouput Layer
for inFeature in spz_lyr:
    # Create output Feature
    tmpFeature = ogr.Feature(tmpLayerDefn)
    # Add field values from input Layer
    for kk in range(0, tmpLayerDefn.GetFieldCount()):
        tmpFeature.SetField(tmpLayerDefn.GetFieldDefn(kk).GetNameRef(), inFeature.GetField(kk))
    # Set geometry as centroid
    geom = inFeature.GetGeometryRef()
    centroid = geom.Centroid()
    tmpFeature.SetGeometry(centroid)
    # Add new feature to output Layer
    tmpLayer.CreateFeature(tmpFeature)

outputs = {}
shpDriver = ogr.GetDriverByName("ESRI Shapefile")
luz_ds = shpDriver.Open(luz, 0)
luz_lyr = luz_ds.GetLayer()
out_model = 'scag-city/input'
#out_model1 = 'scag-city-1/input'
#out_model2 = 'scag-city-2/input'
i = 0
for csa in range(1, 302):
	#if csa % 2 == 1:
	#	out_model = out_model1
	#else:
	#	out_model = out_model2
	# prep output files
	out_zones = open(os.path.join(out_model, 'zones.csv'), 'wb')
	zoneWriter = csv.writer(out_zones, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	zoneWriter.writerow(zones_header)
	out_accatt = open(os.path.join(out_model, 'agents_zones.csv'), 'wb')
	accattWriter = csv.writer(out_accatt, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	accattWriter.writerow(accatt_header)
	out_re = open(os.path.join(out_model, 'real_estates_zones.csv'), 'wb')
	reWriter = csv.writer(out_re, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	reWriter.writerow(re_header)
	out_ba = open(os.path.join(out_model, 'bids_adjustments.csv'), 'wb')
	baWriter = csv.writer(out_ba, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	baWriter.writerow(["H_IDX","V_IDX","I_IDX","BIDADJ"])
	out_ra = open(os.path.join(out_model, 'rent_adjustments.csv'), 'wb')
	raWriter = csv.writer(out_ra, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	raWriter.writerow(["V_IDX","I_IDX","RENTADJ"])
	out_phi = open(os.path.join(out_model, 'demand_exogenous_cutoff.csv'), 'wb')
	phiWriter = csv.writer(out_phi, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	phiWriter.writerow(["H_IDX","V_IDX","I_IDX","DCUTOFF"])
	out_sub = open(os.path.join(out_model, 'subsidies.csv'), 'wb')
	subWriter = csv.writer(out_sub, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	subWriter.writerow(["H_IDX","V_IDX","I_IDX","SUBSIDIES"])
	out_supply = open(os.path.join(out_model, 'supply.csv'), 'wb')
	supplyWriter = csv.writer(out_supply, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
	supplyWriter.writerow(["V_IDX","I_IDX","NREST"])
	luz_lyr.SetAttributeFilter("CSA = " + str(csa))
	for zpoly in luz_lyr:
		i_idx = int(zpoly.GetField("LUZ"))
		bdy = zpoly.GetGeometryRef()
		tmpLayer.SetSpatialFilter(bdy)
		for spz_point in tmpLayer:
			spz_id = spz_point.GetField("SPZID") # keep track of true id
			i += 1 # zone enumeration
			outputs[i] = [spz_id] + [0]*9 # prep to store outputs - id followed by array of "rents"
			zones_row = [i] + zonesDict[i_idx]
			zoneWriter.writerow(zones_row)
			#iterate over agents
			for h in range(1, 10):
				accattRow = [h, i] + accattDict[(h, i_idx)]
				accattWriter.writerow(accattRow)
			# inventory real estate supply
			sfa = spz_point.GetField("du_attsf")
			if sfa > 0:
				sfa_sf = spz_point.GetField("bldg_sqft_attsf") / sfa
			else:
				sfa_sf = 0
			sfd = spz_point.GetField("du_detsf")
			if sfd > 0:
				sfd_sf = (spz_point.GetField("bldg_sqft_detsf_sl") + spz_point.GetField("bldg_sqft_detsf_ll")) / sfd
			else:
				sfd_sf = 0
			mfd = spz_point.GetField("du_mf")
			if mfd > 0:
				mfd_sf = spz_point.GetField("bldg_sqft_mf") / mfd
			else:
				mfd_sf = 0
			ret = spz_point.GetField("emp_retail_services")
			if ret > 0:
				ret_sf = spz_point.GetField("bldg_sqft_retail_services") / ret
			else:
				ret_sf = 0
			ser = spz_point.GetField("emp_restaurant") + spz_point.GetField("emp_accommodation") + spz_point.GetField("emp_arts_entertainment") + spz_point.GetField("emp_other_services") + spz_point.GetField("emp_office_services") + spz_point.GetField("emp_public_admin") + spz_point.GetField("emp_education") + spz_point.GetField("emp_medical_services")
			if ser > 0:
				ser_sf = (spz_point.GetField("bldg_sqft_restaurant") + spz_point.GetField("bldg_sqft_accommodation") + spz_point.GetField("bldg_sqft_arts_entertainment") + spz_point.GetField("bldg_sqft_other_services") + spz_point.GetField("bldg_sqft_office_services") + spz_point.GetField("bldg_sqft_public_admin") + spz_point.GetField("bldg_sqft_education") + spz_point.GetField("bldg_sqft_medical_services")) / ser
			else:
				ser_sf = 0
			man = spz_point.GetField("emp_manufacturing")
			twu = spz_point.GetField("emp_transport_warehousing")
			if twu > 0:
				twu_sf = spz_point.GetField("bldg_sqft_transport_warehousing") / twu
			else:
				twu_sf = 0
			oth = spz_point.GetField("emp_utilities") + spz_point.GetField("emp_construction") + spz_point.GetField("emp_agriculture") + spz_point.GetField("emp_extraction")
			supply = [sfa,sfd,mfd,0,0,ret,ser,man,twu,oth]
			sfunit = [sfa_sf,sfd_sf,mfd_sf,0,0,ret_sf,ser_sf,0,twu_sf,0]
			# iterate over real estate types
			for v in range(1, 10):
				m = reDict[(v,i_idx)][0]
				re_row = [v, i] + reDict[(v,i_idx)]
				if sfunit[v-1] > 0:
					re_row[3] = sfunit[v-1]
				reWriter.writerow(re_row)
				supplyWriter.writerow([v, i, supply[v-1]]) 
				raWriter.writerow([v,i,0])
				for h in range(1,29):
					if agentDict[h] == m:
						phi = 1
					else:
						phi = 0
					phiWriter.writerow([h,v,i,phi])
					subWriter.writerow([h,v,i,0])
					baWriter.writerow([h,v,i,0])
	out_zones.close()
	out_accatt.close()
	out_re.close()
	out_ra.close()
	out_phi.close()
	out_sub.close()
	out_supply.close()
	if os.path.exists("scag-city/output"):
		shutil.rmtree("scag-city/output")
	muland = subprocess.Popen("mu-land scag-city", shell=True)
	muland.wait()
	with open("scag-city/output/rents.csv", 'rb') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=";")
		for row in reader:
			v = int(row['Realestate'])
			j = int(row['Zone'])
			outputs[j][v] = float(row['Value'])
out_file = open("combined_rent_results_2012.csv", 'wb')
outWriter = csv.writer(out_file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
for out_row in outputs:
	outWriter.writerow(outputs[out_row])
out_file.close()
