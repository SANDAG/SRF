## Test script to run mu-Land (with FresnoCOG Envision Tomorrow case study)
## by: Colby M Brown, AICP PTP
## Principal and Founder, Manhan Group LLC
## e-mail: colby@manhangroup.com

#standard library imports
import sys, os, csv, time
from osgeo import ogr
# use OGR specific exceptions
ogr.UseExceptions()
# get drivers
shpDriver = ogr.GetDriverByName("ESRI Shapefile")
tmpDriver = ogr.GetDriverByName("MEMORY")
# input files
TAZ = r'E:\Manhan_Group\LincolnInstitute\FresnoCOG\Fresno_TAZ.shp'

scn_ar = ['ScenarioA_SmallArea','ScenarioB_SmallArea','ScenarioC_SmallArea','Scenario_D']
parcel_dir = r'E:\Manhan_Group\LincolnInstitute\FresnoCOG\SCS_SmallArea_Shapes'
supply_dir = r'E:\Manhan_Group\LincolnInstitute\FresnoCOG'

# output data
for scn in scn_ar:
    print "Running scenario " + scn
    parcel = os.path.join(parcel_dir, scn + ".shp")
    supply_csv = os.path.join(supply_dir, scn + "_supply.csv")
    out_supply = open(supply_csv, 'wb')
    supplyWriter = csv.writer(out_supply, delimiter=";", quoting=csv.QUOTE_NONNUMERIC)
    supplyWriter.writerow(["V_IDX","TAZ_MIP","NREST"])

    # open datasource
    parcel_ds = shpDriver.Open(parcel, 0)
    parcel_lyr = parcel_ds.GetLayer()

    print "Building parcel centroids...",
    start = time.time()
    # Create an in-memory Layer
    tmpDataSource = tmpDriver.CreateDataSource('centroids')
    tmp=tmpDriver.Open('centroids',1)
    tmpLayer = tmpDataSource.CreateLayer("parcel_centroids", geom_type=ogr.wkbPoint)
    # Add input Layer Fields to the output Layer
    inLayerDefn = parcel_lyr.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        tmpLayer.CreateField(fieldDefn)
    # Get the output Layer's Feature Definition
    tmpLayerDefn = tmpLayer.GetLayerDefn()
    # Add features to the ouput Layer
    for inFeature in parcel_lyr:
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
    end = time.time()
    elapsed = end - start
    minutes = int(elapsed / 60)
    seconds = round(elapsed % 60)
    print "completed in %0.0f minutes %0.0f seconds." % (minutes, seconds)


    # iterate through the zones and generate the supply inventory based upon parcel data
    loclist = [] # a list of point locations (zone centroids)
    zones = [] # a separate list -- to keep track of zone IDs
    TAZ_ds = shpDriver.Open(TAZ, 0)
    TAZ_lyr = TAZ_ds.GetLayer()
    for zone in TAZ_lyr:
        i = zone.GetField("TAZ_MIP")
        print 'Zone ' + str(int(i))
        bdy = zone.GetGeometryRef()
        tmpLayer.SetSpatialFilter(bdy)
        supply = [0,0,0,0,0,0] # initialize counts of six dwelling unit types
        for p_point in tmpLayer: # iterate over parcels in zone
            supply[0] += p_point.GetField("SF")
            supply[1] += p_point.GetField("MF")
            supply[2] += p_point.GetField("RET")
            supply[3] += p_point.GetField("OFF")
            supply[4] += p_point.GetField("IND")
            # "Other" works a bit differently (although EMP might actually be sum of other three)
            supply[5] += p_point.GetField("EMP")-(p_point.GetField("RET")+p_point.GetField("OFF")+p_point.GetField("IND"))
        for rex in range(0, 6):
            v = rex + 1
            supplyWriter.writerow([v,i,supply[rex]])
    out_supply.close()
    tmpDataSource.Destroy()
    parcel_ds.Destroy()
    TAZ_ds.Destroy()
