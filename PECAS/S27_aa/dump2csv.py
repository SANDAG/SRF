import csv
import logging
import os
from os.path import join, basename

from psycopg2 import extras

import aa_routines as pr
from scriptutil import irange
from sqlutil import Querier


#_ps = pr._ps
curfact = extras.NamedTupleCursor

def dump_techopt(connect, scendir):
    tr = set_tr(connect)    
    with tr:
        update_techopt(tr, scendir)
    
def _script_dir(fname):
    return join("AllYears", "Code", "technology_scaling_scripts", fname)



def dump_2_csv(tr, sql, outfpath):
    if os.path.exists(outfpath):
        pass
    else:
        tr.dump_to_csv(sql, outfpath)

def set_tr(connect):
    querier = Querier(connect, debug_log=Logger())
    return querier.transaction(cursor_factory=curfact)

def update_techopt(tr, scendir):
    logging.info("Writing TechnologyOptionsI out in csv")
    result = tr.query(
        "select activity, option_name, option_weight, put_name_code, coefficient "
        "from tech_opt.technology_options")

    updates = dict_from_query(result)
    header = read_techopt(scendir)

    outfname = join(scendir, "AllYears", "Inputs",  "TechnologyOptionsI.csv")
    with open(outfname, "w", newline="") as outf:
        writer = csv.writer(outf)
        writer.writerow(header)

        for act in updates:
            for opt in updates.get(act, {}):
                update_row = updates.get(act, {}).get(opt, {})
                new_row = [0]*len(header)
                new_row[0] = act
                new_row[1] = opt
                new_row[2] = update_row['option_weight']
                for i, put in enumerate(header[2:], 2):
                    if put in update_row:
                        new_row[i] = update_row[put]
                writer.writerow(new_row)
           
            


def dict_from_query(result):
    tbl = {}
    for row in result:
        by_act = tbl.setdefault(row.activity, {})
        by_opt = by_act.setdefault(row.option_name, {})
        by_opt['option_weight'] = row.option_weight
        by_opt[row.put_name_code] = row.coefficient
    return tbl


def write_techopt_header(scendir):
    infname = join("E:/PECAS/S21u_m/AllYears", "Inputs", "TechnologyOptionsI.csv")
    outfname = join(scendir, "AllYears", "Inputs", "TechnologyOptionsI_header.csv")
    with open(infname, "r") as inf:
        reader = csv.reader(inf)
        header = next(reader)
    with open(outfname, "w", newline="") as outf:
        writer = csv.writer(outf)
        writer.writerow(header)   


def read_techopt(scendir):
    infname = join(scendir, "AllYears", "Inputs", "TechnologyOptionsI_header.csv")
    with open(infname, "r") as inf:
        reader = csv.reader(inf)
        header = next(reader)
        return header


class Logger:
    # noinspection PyMethodMayBeStatic
    def log(self, text):
        logging.info(text)

# sample use convert_2csv('s21u_m_aa', '^_\d{4}.+') will convert all tables starting with _year to csv
def dump_pg_tbls(connect, scendir, tbl_schema,tname_pattern):
    tr = set_tr(connect)    
    with tr:
        tbls = tr.query("select * from split_tblname('" + tbl_schema + "', '" + tname_pattern + "');")
                        
        for r in tbls:
            flder =r[0]
            fname = r[1]
            tname = r[2] 
            if flder == 'Inputs':
                flder = 'Allyears/Inputs'
            elif flder == 'zz':
                flder = '2016'
                fname = 'zz_' + fname
            
                
            flder = os.path.join(scendir,flder)
                       
            destfile = os.path.join(flder, fname+'.csv')
            if not os.path.exists(flder):
                os.mkdir(flder)
                
            sql = 'select * from \"{}\".\"{}\"'.format(tbl_schema,tname)
# =============================================================================
#             if tname=='Inputs_ExchangeImportExportI':
#                 sql = 'select "ZoneNumber","Commodity","BuyingSize","SellingSize", \
#                 case when "SpecifiedExchange" then ''true''::text else ''false''::text end as "SpecifiedExchange", \
#                 "ImportFunctionMidpoint", \
#                 "ImportFunctionMidpointPrice", \
#                 "ExportFunctionMidpoint", \
#                 "ExportFunctionMidpointPrice",\
#                 "ImportFunctionDelta",\
#                 "ImportFunctionSlope",\
#                 "ImportFunctionEta",\
#                 "ExportFunctionDelta",\
#                 "ExportFunctionSlope",\
#                 "ExportFunctionEta",\
#                  case when "MonitorExchange" then ''true''::text else ''false''::text end as "MonitorExchange" \
#                  from \"{}\".\"{}\"'.format(tbl_schema,tname)
# =============================================================================
            dump_2_csv(tr, sql, destfile)
    
      


if __name__ == "__main__":
    import aa_settings as main_ps


    pr.set_up_logging()
    #write_techopt_header(main_ps.scendir)
    dump_techopt(lambda: pr.connect_to_aa(ps=main_ps), ".") #download the pg friendly techopt file into csv crosstab format
    
    #write yearly AA input to csv
    #dump_pg_tbls(lambda: pr.connect_to_aa(ps=main_ps), ".", 's21u_m_aa','.+')  #dowdload every table in schema s21u_m_aa
   # dump_pg_tbls(lambda: pr.connect_to_aa(ps=main_ps), ".", 's21u_m_aa','^Inputs_')  #download table in Inputs folder
   # dump_pg_tbls(lambda: pr.connect_to_aa(ps=main_ps), ".", 's21u_m_aa','^\d+') #download yearly inputs
   # dump_pg_tbls(lambda: pr.connect_to_aa(ps=main_ps), ".", 's21u_m_aa','^zz_')  #download zz squeeze skim tables
    
    #dump_pg_tbls(lambda: pr.connect_to_aa(ps=main_ps), ".", 's21u_m_aa','^Inputs_ExchangeImportExportI')