# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 02:34:31 2020

@author: MANHAN GROUP
"""
import pandas, os, numpy as np
from utils.interface import save_to_file

# def compressLocation(combined_location):
#     cl_df_wide = pandas.read_csv(combined_location, dtype=np.float64)
#     cl_df_long = pandas.melt(cl_df_wide, id_vars=['Realestate','Zone'], var_name='AgentType', value_name='Value').set_index(['Realestate','Zone'])
#     agentXtype = cl_df_long.agg(func=np.sum, axis='index').pivot(index='Zone', columns='Realestate', values='Value')
#     agentXtype.columns = ['mgra','hh_sf','hh_mf','hh_mh','emp_ind','emp_com','emp_ofc','emp_oth']
#     return agentXtype

def updateSupply(combined_location,combined_rent,old_supply_input,new_supply_input=None):
    print("update supply input data")
    r_df = pandas.read_csv(combined_rent, dtype={'Value': np.float64}, na_values = np.NaN, index_col=['Realestate','Zone'])
    r_df = r_df.replace([np.inf, -np.inf], np.nan)
    #r_df = r_df.replace(np.inf, max(r_df[r_df.Value!=np.inf].Value))
    #r_df = r_df.replace(-np.inf, min(r_df[r_df.Value!=-np.inf].Value))
    #r_df = r_df.clip(lower=0.1)
    #r_df = r_df.clip(upper=50000)

    s_df = pandas.read_csv(old_supply_input,dtype={'valueSFmea': np.float64, 'valueMFmea': np.float64,
                                                   'valueINDme': np.float64, 'valueCOMme': np.float64,
                                                   'valueOFCme': np.float64}, index_col='MGRA')

    cl_df_wide = pandas.read_csv(combined_location, dtype=np.float64)
    cl_df_long = pandas.melt(cl_df_wide, id_vars=['Realestate','Zone'], var_name='AgentType', value_name='Value').set_index(['Realestate','Zone'])
    agentXtype = cl_df_long.agg(func=np.sum, axis='index').pivot(index='Zone', columns='Realestate', values='Value')
    agentXtype.columns = ['mgra','hh_sf','hh_mf','hh_mh','emp_ind','emp_com','emp_ofc','emp_oth']                   
    agentXtype = agentXtype.replace([np.inf, -np.inf], np.nan)
    s_df = s_df.join(agentXtype[['mgra','hh_sf','hh_mf','hh_mh','emp_ind','emp_ofc','emp_com','emp_oth']], rsuffix="_new", sort=True)
    s_df['hh_sf'] = s_df['hh_sf_new']
    s_df['hh_mf'] = s_df['hh_mf_new']
    s_df['hh_mh'] = s_df['hh_mh_new']
    s_df['hh'] = s_df['hh_sf'] + s_df['hh_mf'] + s_df['hh_mh']
    s_df['emp_indus_'] = s_df['emp_ind']
    s_df['emp_office'] = s_df['emp_ofc']
    s_df['emp_comm_l'] = s_df['emp_com']
    s_df['emp_other_'] = s_df['emp_oth']
    s_df.drop(['mgra','hh_sf_new','hh_mf_new','hh_mh_new','emp_ind','emp_ofc','emp_com','emp_oth'])

    ## TODO: Update employment by real estate type as well

# =============================================================================
#     s_df['valueSFmea'] = r_df.xs(1)['Value'].fillna(s_df['valueSFmea'])
#     s_df['valueMFmea'] = r_df.xs(2)['Value'].fillna(s_df['valueMFmea'])
#     s_df['valueINDme'] = r_df.xs(4)['Value'].fillna(s_df['valueINDme'])
#     s_df['valueCOMme'] = r_df.xs(5)['Value'].fillna(s_df['valueCOMme'])
#     s_df['valueOFCme'] = r_df.xs(6)['Value'].fillna(s_df['valueOFCme'])
# =============================================================================

    min_sdf = s_df[['valueSFmea','valueMFmea','valueINDme','valueCOMme','valueOFCme']].min()
    max_sdf = s_df[['valueSFmea','valueMFmea','valueINDme','valueCOMme','valueOFCme']].max()
    s_df['valueSFmea'] = r_df.xs(1)['Value'].fillna(s_df['valueSFmea']).clip(lower=0.8*min_sdf['valueSFmea']).clip(upper=1.2*max_sdf['valueSFmea'])
    s_df['valueMFmea'] = r_df.xs(2)['Value'].fillna(s_df['valueMFmea']).clip(lower=0.8*min_sdf['valueMFmea']).clip(upper=1.2*max_sdf['valueSFmea'])
    s_df['valueINDme'] = r_df.xs(4)['Value'].fillna(s_df['valueINDme']).clip(lower=0.8*min_sdf['valueINDme']).clip(upper=1.2*max_sdf['valueSFmea'])
    s_df['valueCOMme'] = r_df.xs(5)['Value'].fillna(s_df['valueCOMme']).clip(lower=0.8*min_sdf['valueCOMme']).clip(upper=1.2*max_sdf['valueSFmea'])
    s_df['valueOFCme'] = r_df.xs(6)['Value'].fillna(s_df['valueOFCme']).clip(lower=0.8*min_sdf['valueOFCme']).clip(upper=1.2*max_sdf['valueSFmea'])

# =============================================================================
#     s_df['valueSFmea'] = np.maximum(0.8*s_df['valueSFmea'],np.minimum(s_df['valueSFmea']*1.2,r_df.xs(1)['Value'].fillna(s_df['valueSFmea'])))
#     s_df['valueMFmea'] = np.maximum(0.8*s_df['valueMFmea'],np.minimum(s_df['valueMFmea']*1.2,r_df.xs(2)['Value'].fillna(s_df['valueMFmea'])))
#     s_df['valueINDme'] = np.maximum(0.8*s_df['valueINDme'],np.minimum(s_df['valueINDme']*1.2,r_df.xs(4)['Value'].fillna(s_df['valueINDme'])))
#     s_df['valueCOMme'] = np.maximum(0.8*s_df['valueCOMme'],np.minimum(s_df['valueCOMme']*1.2,r_df.xs(5)['Value'].fillna(s_df['valueCOMme'])))
#     s_df['valueOFCme'] = np.maximum(0.8*s_df['valueOFCme'],np.minimum(s_df['valueOFCme']*1.2,r_df.xs(6)['Value'].fillna(s_df['valueOFCme'])))
#
# =============================================================================

    s_df = s_df.reset_index()
    if (new_supply_input is not None):
        outdir, fname = os.path.split(new_supply_input)
        save_to_file(s_df, outdir, fname)
    return s_df

# if __name__ == "__main__":
#     import time
#     import sys
#     start_time = time.time()
#     combined_rent = r"D:\PECAS\SRF.git\branches\Supply\profitability-adjusters\Demand\2012\combined_rents.csv"
#     old_supply_input = r"D:\PECAS\SRF.git\branches\Supply\profitability-adjusters\Supply\data\supply_input_2013.csv"
#     new_supply_input = r"D:\PECAS\SRF.git\branches\Supply\profitability-adjusters\Supply\data\supply_input_2013n.csv"
#
#     importRents(combined_rent,old_supply_input,new_supply_input)
#     print("---%s seconds ---" % (time.time() - start_time))
