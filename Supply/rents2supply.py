# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 02:34:31 2020

@author: MANHAN GROUP
"""
import pandas, os, numpy as np
from utils.interface import save_to_file

def importRents(combined_rent,old_supply_input,new_supply_input=None):
    r_df = pandas.read_csv(combined_rent, dtype={'Value': np.float64}, na_values = np.NaN, index_col=['Realestate','Zone'])
    #r_df = r_df.replace([np.inf, -np.inf], np.nan)
    #r_df = r_df.replace(np.inf, max(r_df[r_df.Value!=np.inf].Value))
    #r_df = r_df.replace(-np.inf, min(r_df[r_df.Value!=-np.inf].Value))
    r_df = r_df.clip(lower=0.1)
    r_df = r_df.clip(upper=50000)
    
    s_df = pandas.read_csv(old_supply_input,dtype={'valueSFmea': np.float64, 'valueMFmea': np.float64,
                                                   'valueINDme': np.float64, 'valueCOMme': np.float64, 
                                                   'valueOFCme': np.float64}, index_col='MGRA')
    
    s_df['valueSFmea'] = r_df.xs(1)['Value'].fillna(s_df['valueSFmea'])
    s_df['valueMFmea'] = r_df.xs(2)['Value'].fillna(s_df['valueMFmea'])
    s_df['valueINDme'] = r_df.xs(4)['Value'].fillna(s_df['valueINDme'])
    s_df['valueCOMme'] = r_df.xs(5)['Value'].fillna(s_df['valueCOMme'])
    s_df['valueOFCme'] = r_df.xs(6)['Value'].fillna(s_df['valueOFCme'])
    
    s_df = s_df.reset_index()
    if (new_supply_input is not None):
        outdir, fname = os.path.split(new_supply_input)
        save_to_file(s_df, outdir, fname)
    return s_df

if __name__ == "__main__":
    import time
    import sys
    start_time = time.time()
    combined_rent = sys.argv[1]
    old_supply_input = sys.argv[2]
    new_supply_input = sys.argv[3]

    importRents(combined_rent,old_supply_input,new_supply_input)
    print("---%s seconds ---" % (time.time() - start_time))