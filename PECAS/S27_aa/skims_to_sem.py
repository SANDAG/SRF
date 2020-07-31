import csv
import logging
from os.path import join
import itertools
import shutil

import aa_routines as pr
from aa_routines import _ps
from scriptutil import irange, backup_name
import csvutil as cu

# To run on the command line:
# python skims_to_sem.py <skim year>

import numexpr as ne
#HERE: reset number of vml-threads
ne.set_vml_num_threads(16)

def main(year, ps=_ps):
    externals = irange(230, 236)
    
    convert_skims(
        ps, year,
        skim_names=[
            "AM_SOV_TR_M_DIST",
            "AM_SOV_TR_M_TIME",
            "AM_SOV_TR_M_TOLLCOST",
        ],
        sql_fname="skim_conversion_for_sem_sov.sql",
        taz_skims_fname="TazSkimsSOV.csv",
        luz_skims_fname="SkimsISOV.csv",
        omx_fname="traffic_skims_AM.omx",
        table_suffix="sov",
        check_skim="AM_SOV_TR_M_TIME",
        externals=externals,
    )
    
    transit_access = TransitAccess(
        ps, year,
        stations_tname="TapToTaz",
        access_skim_fname="TazSkimsSOV.csv",
        access_skim_names=[
            "AM_SOV_TR_M_DIST",
            "AM_SOV_TR_M_TIME",
            "AM_SOV_TR_M_TOLLCOST",
        ],
        access_skim="AM_SOV_TR_M_DIST",
        access_walk_speed=0.05,
        externals=externals,
    )
    
    convert_skims(
        ps, year,
        skim_names=[
            "AM_ALLPEN_TOTALIVTT",
            "AM_ALLPEN_TOTALWAIT",
            "AM_ALLPEN_TOTALWALK",
            "AM_ALLPEN_XFERS",
        ],
        sql_fname="skim_conversion_for_sem_transit.sql",
        transit_access=transit_access,
        taz_skims_fname="TazSkimsTransit.csv",
        luz_skims_fname="SkimsITransit.csv",
        omx_fname="transit_skims.omx",
        table_suffix="transit",
        remove_if="am_allpen_totalivtt = 0",
        check_skim="AM_ALLPEN_TOTALIVTT",
        externals=externals,
    )
    
    convert_skims(
        ps, year,
        skim_names=[
            "MD_TRK_M_DIST",
            "MD_TRK_M_TIME",
            "MD_TRK_M_TOLLCOST",
        ],
        target_skim_names=[
            "dist_da_t_op",
            "time_da_t_op",
            "toll_op",
        ],
        sql_fname="skim_conversion_for_sem_goods.sql",
        taz_skims_fname="TazSkimsGoods.csv",
        luz_skims_fname="SkimsIGoods.csv",
        omx_fname="traffic_skims_MD.omx",
        table_suffix="goods",
        check_skim="MD_TRK_M_TIME",
        externals=externals,
    )
    
    combine(
        join(ps.scendir, str(year), ps.skim_fname.format(yr=year) + ".csv"),
        join(ps.scendir, str(year), "SkimsIGoods.csv"),
        join(ps.scendir, str(year), "SkimsISOV.csv"),
        join(ps.scendir, str(year), "SkimsITransit.csv"),
        available_flags=[None, None, "transit_available"]
    )


class TransitAccess:
    def __init__(
        self, ps, year,
        stations_tname,
        access_skim_fname,
        access_skim_names,
        access_skim, # Assume this is time...
        access_walk_speed=None, # unless we specify a walk speed. Then, it's distance and we convert.
        externals=[],
    ):
        self.ps = ps
        #self.stations_path = join(ps.inputpath, stations_fname)
        self.stations_path =  '{}.\"{}\"'.format(ps.aa_schema, stations_tname)
        self.access_skim_path = join(ps.scendir, str(year), access_skim_fname)
        self.access_skim_fields = skim_fields_for_query([skim_name.lower() for skim_name in access_skim_names])
        self.access_skim = access_skim.lower()
        self.access_walk_speed = access_walk_speed
        self.externals = externals
        
    
    def create_skims_with_access(self, querier, station_skims_path, skim_names, taz_skims_path):
        ps = self.ps
        
        def schemify(name):
            return "{}.zz_transit_access_{}".format(ps.sd_schema, name)
        
        station_tblname = schemify("stations")
        access_skim_tblname = schemify("access_skims")
        station_skim_tblname = schemify("station_skims")
        taz_skim_tblname = schemify("taz_skims")
        
        
        args = dict(
            stationtbl=station_tblname,
            access_skimtbl=access_skim_tblname,
            station_skimtbl=station_skim_tblname,
            taz_skimtbl=taz_skim_tblname,
            access_skim=self.access_skim.lower(),
            ori_stations_tbl=self.stations_path
        )
        
        with querier.transaction(**args) as tr:
            #tr.query("drop table if exists {stationtbl}")
            #tr.query("create table {stationtbl} (station integer primary key, taz integer)")
            #tr.load_from_csv(station_tblname, self.stations_path)
            #tr.query("insert into {stationtbl} select * from {ori_stations_tbl}")

            tr.query("create view {stationtbl} as select * from {ori_stations_tbl}")
            
            tr.query("drop table if exists {access_skimtbl}")
            tr.query(
                "create table {access_skimtbl} (\n"
                "   origin integer,\n"
                "   destination integer,\n" +
                self.access_skim_fields + "\n"+
                ")"
            )
            tr.load_from_csv(access_skim_tblname, self.access_skim_path)
            tr.query(
                "delete from {access_skimtbl} where origin in %(externals)s or destination in %(externals)s",
                externals=tuple(self.externals)
            )
            
            tr.query("alter table {access_skimtbl} add column access_skim double precision")
            if self.access_walk_speed is None:
                tr.query("update {access_skimtbl} set access_skim = {access_skim}")
            else:
                tr.query(
                    "update {access_skimtbl} set access_skim = {access_skim} / {walk_speed}",
                    walk_speed=self.access_walk_speed
                )
            tr.query("alter table {access_skimtbl} add primary key(origin, destination)")

            tr.query("drop table if exists {station_skimtbl}")
            tr.query(
                "create table {station_skimtbl} (\n"
                "   origin_station integer,\n"
                "   destination_station integer,\n" +
                skim_fields_for_query(skim_names) + "\n" +
                ")"
            )
            tr.load_from_csv(station_skim_tblname, station_skims_path)
            tr.query("alter table {station_skimtbl} add primary key(origin, destination)")

            tr.query("analyze {access_skimtbl}")
            tr.query("analyze {station_skimtbl}")
         
        with querier.transaction(**args) as tr:   
            tr.query_external("transit_access.sql")
            tr.dump_to_csv("select * from {taz_skimtbl}", taz_skims_path)
    

def convert_skims(
    ps, year,
    skim_names,
    target_skim_names=None,
    #transport_zones_fname="TransportZones.csv",
    transport_zones_tname="TransportZones",
    sql_fname="skim_conversion_for_sem.sql",
    transit_access=None,
    #station_numbers_fname="StationNumbers.csv",
    station_numbers_tname="StationNumbers",
    taz_skims_fname=None,
    luz_skims_fname=None,
    omx_fname=None,
    table_suffix=None,
    remove_if="false",
    check_skim=None,
    externals=[],
):
    if target_skim_names is None:
        target_skim_names = [name.lower() for name in skim_names]
    if taz_skims_fname is None:
        taz_skims_fname = ps.taz_skims_fname.format(yr=year) + ".csv"
    if luz_skims_fname is None:
        luz_skims_fname = ps.skim_fname.format(yr=year) + ".csv"
    
    querier = pr.aa_querier(ps=ps)
    
    #transport_zones_path = join(ps.inputpath, transport_zones_fname)
    #station_numbers_path = join(ps.inputpath, station_numbers_fname)
    transport_zones_path = '{}.\"{}\"'.format(ps.aa_schema, transport_zones_tname)
    station_numbers_path = '{}.\"{}\"'.format(ps.aa_schema, station_numbers_tname)
    taz_skims_path = join(ps.scendir, str(year), taz_skims_fname)
    
    if omx_fname is not None:
        omx_path = join(ps.scendir, str(year), omx_fname)
        labels_path = transport_zones_path if transit_access is None else station_numbers_path
        extract_from_omx(omx_path, skim_names, labels_path, taz_skims_path,ps=ps)
    
    if transit_access is not None:
        logging.info("Adding transit access")
        station_skims_path = join(ps.scendir, str(year), backup_name(taz_skims_fname, "Stations"))
        shutil.copy(taz_skims_path, station_skims_path)
        transit_access.create_skims_with_access(querier, station_skims_path, target_skim_names, taz_skims_path)

    def schemify(name):
        suffix = "" if table_suffix is None else "_" + table_suffix
        return "{}.zz_skim_squeeze{}_{}".format(ps.sd_schema, suffix, name)

    taz_tblname = schemify("tdm_zones")
    #world_tblname = schemify("world_zone_skims")
    #midday_tblname = schemify("midday_flows")
    world_tblname = '{}.\"{}\"'.format(ps.aa_schema, "world_zone_skims")
    midday_tblname = '{}.\"{}\"'.format(ps.aa_schema, "MiddayFlows")
    tdm_skim_tblname = schemify("tdm_skims")
    taz_skim_tblname = schemify("taz_skims")
    luz_skim_tblname = schemify("luz_skims")

    args = dict(
        taztbl=taz_tblname, worldtbl=world_tblname, middaytbl=midday_tblname,
        tdm_skimtbl=tdm_skim_tblname, taz_skimtbl=taz_skim_tblname,
        luz_skimtbl=luz_skim_tblname,
        transport_zones_tbl = transport_zones_path
    )

    with querier.transaction(**args) as tr:
        skim_fields = skim_fields_for_query(target_skim_names)
        
        logging.info("Loading zone info")

        #tr.query("drop table if exists {taztbl}")
        #tr.query("create table {taztbl} (tdm_taz integer, luz integer)")
        #tr.load_from_csv(taz_tblname, transport_zones_path)
        tr.query("create view {taztbl} as select taz as tdm_taz,luz from {transport_zones_tbl}")
        
       # tr.query("drop table if exists {worldtbl}")
       # tr.query(
        #   "create table {worldtbl} (\n"
        #    "   worldmarket integer,\n"
        #    "   externalstation integer,\n"
        #    "   \"time\" double precision,\n"
        #    "   distance double precision\n"
        ##    ")"
        #)
        #tr.load_from_csv(world_tblname, join(ps.inputpath, "WorldZoneSkims.csv"))

        #tr.query("drop table if exists {middaytbl}")
        #tr.query("create table {middaytbl} (i integer, j integer, flows double precision, primary key (i, j))")
        #tr.query("Alter table {middaytbl} add primary key (i, j)")
        #tr.load_from_csv(midday_tblname, join(ps.inputpath, "MiddayFlows.csv"))

        tr.query("drop table if exists {tdm_skimtbl}")

        tr.query(
            "create table {tdm_skimtbl} (\n"
            "   origin integer,\n"
            "   destination integer,\n" +
            skim_fields +
            ")"
        )

        logging.info("Loading skims for year {}".format(year))
        
        tr.load_from_csv("{tdm_skimtbl}", taz_skims_path)
        tr.query("delete from {tdm_skimtbl} where " + remove_if)
        tr.query("create index on {tdm_skimtbl} (origin,destination)")
        tr.query("analyze {tdm_skimtbl}")

    with querier.transaction(**args) as tr:          
        logging.info("Adding externals")
        
        tr.query_external(sql_fname, end="BREAK")
        
        logging.info("Analyzing")
        
        tr.query("analyze {taz_skimtbl}")
 
    with querier.transaction(**args) as tr:         
        logging.info("Squeezing skims")
        tr.query_external(sql_fname, start="BREAK")
        check_capping(tr, target_skim_names[skim_names.index(check_skim)], externals=externals)
        
        logging.info("Dumping LUZ skims")
        
        tr.dump_to_csv(
            "select * from {luz_skimtbl} order by origin, destination",
            join(ps.scendir, str(year), luz_skims_fname)
        )


def extract_from_omx(omx_fname, skim_names, transport_zones_path, taz_skims_path,ps):
    import openmatrix as omx
    import numpy as np
    logging.info("Extracting skims from {}".format(omx_fname))
    f = omx.open_file(omx_fname)
    try:
        zones = read_zones_pg(transport_zones_path,ps)
        
        matrices = [np.array(f[name]) for name in skim_names]
        
        result = [["i", "j"] + skim_names]
        for i_idx, i in enumerate(zones):
            for j_idx, j in enumerate(zones):
                result.append([i, j] + [matrix[i_idx, j_idx] for matrix in matrices])
        
        write_skims(taz_skims_path, result)
            
    finally:
        f.close()


def read_zones(path):
    with open(path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        taz_col = header.index("taz")
        return [row[taz_col] for row in reader]
        
def read_zones_pg(path,ps):
    querier = pr.aa_querier(ps=ps)
    args = dict(path_tbl = path)
    with querier.transaction(**args) as tr:
        rows = tr.query('select taz from {path_tbl}')
        return [row[0] for row in rows]

def write_skims(path, skim_data):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for row in skim_data:
            writer.writerow(row)


def skim_fields_for_query(skim_names):
    return ",\n".join(
        "   \"{}\" double precision".format(skim_name)
        for skim_name in skim_names
    )

            
def combine(dest_path, *source_paths, available_flags=None):
    if available_flags is None:
        available_flags = itertools.repeat(None)
    source_skims = list(map(read_skims, source_paths))
    keys = sorted(set(source_skims[0].keys()).union(*source_skims[1:]))
    result = {key: [] for key in keys}
    header = ["origin", "destination"]
    for skims, available_flag in zip(source_skims, available_flags):
        skim_names = list(next(iter(skims.values())).keys())
        if available_flag is not None:
            header.append(available_flag)
        header.extend(skim_names)
        for key, row in result.items():
            if available_flag is None:
                if key in skims:
                    row.extend(skims[key].values())
                else:
                    raise ValueError("No skims for origin {}, destination {}".format(*key))
            else:
                if key in skims:
                    row.append("true")
                    row.extend(skims[key].values())
                else:
                    row.append("false")
                    row.extend([0 for name in skim_names])
    result_rows = [header] + [list(key) + row for key, row in result.items()]
    write_skims(dest_path, result_rows)

    
def read_skims(path):
    def row_f(key):
        o, d = key
        return int(o), int(d)
    return cu.read_table(path, rowh_size=2, row_f=row_f, value_f=float)


def check_capping(tr, skim_name, externals):
    result = tr.query(
        "select origin_luz,\n"
        "count(distinct destination_luz) from {taz_skimtbl}\n"
        "where {skim_name} > 2000\n"
        "and origin_luz not in %(externals)s and destination_luz not in %(externals)s\n"
        "group by origin_luz\n"
        "order by count(distinct destination_luz) desc;",
        skim_name=skim_name,
        externals=tuple(externals)
    )
    
    if result:
        logging.error("There are skims over 2000 minutes!")
        for row in result:
            logging.error("Found {} bad skims from origin {}".format(row[1], row[0]))
        raise AssertionError()


if __name__ == "__main__":
    import sys
    import aa_settings as ps
    skim_year = sys.argv[1]
    skim_year = int(skim_year)
    pr.set_up_logging()
    user = pr.db_user(ps)
    ps.sd_schema = user
    import time
    start_time = time.time()
    main(skim_year, ps)
    print("---%s seconds ---" % (time.time() - start_time))
