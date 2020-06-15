# flake8: noqa

"""
Input column names eg.
CONSTANT = 'SANDAG_column_name' # metadata
"""
MGRA = 'MGRA'  # Series 13 MGRA
LUZ = 'LUZ'  # Zone for urban modeling
POPULATION = 'pop'  # Total population
HOUSEHOLD_POPULATION = 'hhp'  # Household population
EMPLOYED_RESIDENTS = 'er'  # Employed residents
GROUP_QUARTERS_POPULATION = 'gq'  # Group quarters population
# Civilian group quarters population
GROUP_QUARTERS_CIVILIAN_POPULATION = 'gq_civ'
# Civilian group quarters population- college dormitory housing
COLLEGE_POPULATION = 'gp_civ_college'
# Civilian group quarters population- other, for example senior housing, homeless pop.'
GROUP_QUARTERS_OTHER_POPULATION = 'gq_civ_other'
MILITARY_POPULATION = 'gq_mil'  # Military group quarters population
HOUSING_UNITS = 'hs'  # Housing units
SINGLE_FAMILY_HOUSING_UNITS = 'hs_sf'  # Single-family housing units
# total squarefootage of single-family units
SINGLE_FAMILY_TOTAL_SQUARE_FOOTAGE = 'sf_sqft'
MULTI_FAMILY_HOUSING_UNITS = 'hs_mf'  # Multiple-family housing units
# total squarefootage of multiple-family units
MULTI_FAMILY_TOTAL_SQUARE_FOOTAGE = 'mf_sqft'
MOBILE_HOUSING_UNITS = 'hs_mh'  # Mobile home housing units
HOUSEHOLDS = 'hh'  # Households (occupied housing units)
# Single-family households (occupied housing units)
SINGLE_FAMILY_HOUSEHOLDS = 'hh_sf'
# Multiple-family households (occupied housing units)
MULTI_FAMILY_HOUSEHOLDS = 'hh_mf'
MOBILE_HOUSEHOLDS = 'hh_mh'  # Mobile home households (occupied housing units)
# total sqarefeet in industrial buildings
INDUSTRIAL_TOTAL_SQUARE_FOOTAGE = 'indus_sqft'
INDUSTRIAL_BUILDINGS = 'units_indus'  # number of industrial buildings
# total squarefeet in commercial/retail buildings
COMMERCIAL_TOTAL_SQUARE_FOOTAGE = 'comm_sqft'
COMMERCIAL_UNITS = 'units_comm'  # number of commercial/retail buildings
# total squarefeet in office buildings
OFFICE_TOTAL_SQUARE_FOOTAGE = 'office_sqft'
OFFICE_UNITS = 'units_office'  # number of office buildings
EMPLOYMENT = 'emp'  # Employment
CIVILIAN_EMPLOYMENT = 'emp_civ'  # Civilian employment
MILITARY_EMPLOYMENT = 'emp_mil'  # Uniformed military personnel
# Non-agricultural civilian wage and salary employment
NON_AGRICULTURE_EMPLOYMENT = 'emp_nonag_civ_ws'
AGRICULTURE_EMPLOYMENT = 'emp_ag'  # Employment in Agriculture and Mining
CONSTRUCTION_EMPLOYMENT = 'emp_con'  # Employment in Construction
MANUFACTURING_EMPLOYMENT = 'emp_mfg'  # Employment in Manufacturing
# Employment in Transportation, Communication and Utilities
TRANSPORTATION_EMPLOYMENT = 'emp_tcpu'
WHOLESALE_TRADE_EMPLOYMENT = 'emp_whtrade'  # Employment in Wholesale Trade
RETAIL_TRADE_EMPLOYMENT = 'emp_retrade'  # Employment in Retail Trade
# Employment in Finance, Insurance and Real Estate
FINANCE_INSURANCE_REAL_ESTATE_EMPLOYMENT = 'emp_fire'
SERVICES_EMPLOYMENT = 'emp_serv'  # Employment in Services
GOVERNMENT_EMPLOYMENT = 'emp_gov'  # Employment in Government
SELF_EMPLOYMENT = 'emp_sedw'  # Number of self-employed persons
INCOME_1 = 'i1'  # Number of households with income less than $15,000
INCOME_2 = 'i2'  # Number of households with income $15,000-$29,999
INCOME_3 = 'i3'  # Number of households with income $30,000-$44,999
INCOME_4 = 'i4'  # Number of households with income $45,000-$59,999
INCOME_5 = 'i5'  # Number of households with income $60,000-$74,999
INCOME_6 = 'i6'  # Number of households with income $75,000-$99,999
INCOME_7 = 'i7'  # Number of households with income $100,000-$124,999
INCOME_8 = 'i8'  # Number of households with income $125,000-$149,999
INCOME_9 = 'i9'  # Number of households with income $150,000-$199,999
INCOME_10 = 'i10'  # Number of households with income $200,000 or more
# acres developed as spaced rural residential; lot sizes of one acre or more
RURAL_DEVELOPED_ACRES = 'dev_ldsf'
# acres developed as single family residential; detached housing units on lots smaller than one acre
SINGLE_FAMILY_DEVELOPED_ACRES = 'dev_sf'
# acres developed as multiple family residential
MULTI_FAMILY_DEVELOPED_ACRES = 'dev_mf'
MOBILE_HOME_DEVELOPED_ACRES = 'dev_mh'  # acres developed as mobile home parks
# acres developed as group quarters residential
GROUP_QUARTERS_DEVELOPED_ACRES = 'dev_oth'
# acres developed as agricultural, extractive industry, or junkyard/dumps/landfills
AGRICULTURE_DEVELOPED_ACRES = 'dev_ag'
# acres developed as industrial, wholesale trade, airport, rail station, communications and utilities, center city parking, park and ride lots, other transportation, or marine terminals
INDUSTRIAL_DEVELOPED_ACRES = 'dev_indus'
# acres developed as retail trade, hotels/motels/resorts, public services, hospitals, or commercial recreation
COMMERCIAL_DEVELOPED_ACRES = 'dev_comm'
OFFICE_DEVELOPED_ACRES = 'dev_office'  # acres developed as offices
SCHOOLS_DEVELOPED_ACRES = 'dev_schools'  # acres developed as schools
# acres developed as freeways, railroads, or surface streets
ROADS_DEVELOPED_ACRES = 'dev_roads'
# acres developed as parks, including beaches and open space
PARKS_DEVELOPED_ACRES = 'dev_parks'
MILITARY_DEVELOPED_ACRES = 'dev_mil'  # acres developed as military use
# acres in bays, lagoons, lakes, reservoirs, and large ponds
WATER_DEVELOPED_ACRES = 'dev_water'
# undeveloped acres planned for spaced rural residential
RURAL_VACANT_ACRES = 'vac_ldsf'
# undeveloped acres planned for single family residential
SINGLE_FAMILY_VACANT_ACRES = 'vac_sf'
# undeveloped acres planned for multiple family residential
MULTI_FAMILY_VACANT_ACRES = 'vac_mf'
# undeveloped acres planned for mobile home parks
MOBILE_HOME_VACANT_ACRES = 'vac_mh'
# undeveloped acres planned for group quarters residential
GROUP_QUARTERS_VACANT_ACRES = 'vac_oth'
# undeveloped acres planned for agricultural, extractive industry, or junkyard/dumps/landfills
AGRICULTURE_VACANT_ACRES = 'vac_ag'
INDUSTRIAL_VACANT_ACRES = 'vac_indus'  # undeveloped acres planned for industrial, wholesale trade, airport, rail station, communications and utilities, center city parking, park and ride lots, other transportation, or marine terminals
# undeveloped acres planned for retail trade, hotels/motels/resorts, public services, hospitals, or commercial recreation
COMMERCIAL_VACANT_ACRES = 'vac_comm'
OFFICE_VACANT_ACRES = 'vac_office'  # undeveloped acres planned for offices
SCHOOLS_VACANT_ACRES = 'vac_schools'  # undeveloped acres planned for schools
# undeveloped acres planned for freeways, railroads, or surface streets
ROADS_VACANT_ACRES = 'vac_roads'
# acres developed as single family residential, planned for redevelopment as multiple family residential
SINGE_FAMILY_MULTI_FAMILY_REDEVELOPMENT_ACRES = 'redev_sf_mf'
# acres developed as single family residential, planned for redevelopment as employment use
SINGE_FAMILY_EMPLOYMENT_REDEVELOPMENT_ACRES = 'redev_sf_emp'
# acres developed as multiple family residential, planned for redevelopment as employment use
MULTI_FAMILY_EMPLOYMENT_REDEVELOPMENT_ACRES = 'redev_mf_emp'
# acres developed as mobile home parks, planned for redevelopment as single family residential
MOBILE_HOME_SINGLE_FAMILY_REDEVELOPMENT_ACRES = 'redev_mh_sf'
# acres developed as mobile home parks, planned for redevelopment as multiple family residential
MOBILE_HOME_MULTI_FAMILY_REDEVELOPMENT_ACRES = 'redev_mh_mf'
# acres developed as mobile home parks, planned for redevelopment as employment use
MOBILE_HOME_EMPLOYMENT_REDEVELOPMENT_ACRES = 'redev_mh_emp'
# acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as spaced rural residential
AGRICULTURE_RURAL_REDEVELOPMENT_ACRES = 'redev_ag_ldsf'
# acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as single family residential
AGRICULTURE_SINGLE_FAMILY_REDEVELOPMENT_ACRES = 'redev_ag_sf'
# acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as multiple family residential
AGRICULTURE_MULTI_FAMILY_REDEVELOPMENT_ACRES = 'redev_ag_mf'
# acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as industrial, wholesale trade, airport, rail station, communications and utilities, center city parking, park and ride lots, other transportation,
AGRICULTURE_INDUSTRIAL_REDEVELOPMENT_ACRES = 'redev_ag_indus'
# acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as retail trade, hotels/motels/resorts, public services, hospitals, or commercial recreation
AGRICULTURE_COMMERCIAL_REDEVELOPMENT_ACRES = 'redev_ag_comm'
# acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as offices
AGRICULTURE_OFFICE_REDEVELOPMENT_ACRES = 'redev_ag_office'
# acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as schools
AGRICULTURE_SCHOOLS_REDEVELOPMENT_ACRES = 'redev_ag_schools'
# acres developed as agricultural, extractive industry, or junkyard/dumps/landfills planned for redevelopment as freeways, railroads, or surface streets
AGRICULTURE_ROADS_REDEVELOPMENT_ACRES = 'redev_ag_roads'
# acres developed as employment use, planned for redevelopment as residential
EMPLOYMENT_RESIDENTIAL_REDEVELOPMENT_ACRES = 'redev_emp_res'
# acres developed as employment use, planned for redevelopment as a different category of employment use
EMPLOYMENT_EMPLOYMENT_REDEVELOPMENT_ACRES = 'redev_emp_emp'
# developed acres planned for single family residential infill
SINGLE_FAMILY_INFILL_ACRES = 'infill_sf'
# developed acres planned for multiple family residential infill
MULTI_FAMILY_INFILL_ACRES = 'infill_mf'
# developed acres planned for employment infill
EMPLOYMENT_INFILL_ACRES = 'infill_emp'
TOTAL_ACRES = 'acres'  # total acres
DEVELOPED_ACRES = 'dev'  # total developed acres
VACANT_ACRES = 'vac'  # total vacant acres
# vacant land not available for development for physical, public policy, or environmental reasons
UNUSABLE_ACRES = 'unusable'
LAND_COST_PER_ACRE = 'Land_Cost'  # cost of land per acre

# # cost of construction per square foot for single family dwelling
# SINGLE_FAMILY_CONSTRUCTION_COST = 'cost_cons_sf'
# # cost of construction per square foot for multi family dwelling
# MULTI_FAMILY_CONSTRUCTION_COST = 'cost_cons_mf'
# # cost of construction per square foot for commercial/retail development
# COMMERCIAL_CONSTRUCTION_COST = 'cost_cons_comm'
# # cost of construction per square foot for industrial development
# INDUSTRIAL_CONSTRUCTION_COST = 'cost_cons_indus'
# # cost of construction per square foot for office development
# OFFICE_CONSTRUCTION_COST = 'cost_cons_office'

# price/rent cost per square foot for single family dwelling
SINGLE_FAMILY_RENT = 'Price_SF'
# price/rent cost per square foot for multi family dwelling
MULTI_FAMILY_RENT = 'Price_MF'
# price/rent cost per square foot for commercial/retail building
COMMERCIAL_RENT = 'Ret_Cost'
# price/rent cost per square foot for industrial building
INDUSTRIAL_RENT = 'Ind_Cost'
OFFICE_RENT = 'Ofc_Cost'  # price/rent cost per square foot for office building
DEV_1 = 'dev1'  # acres assigned with development code 1
DEV_2 = 'dev2'  # acres assigned with development code 2
DEV_3 = 'dev3'  # acres assigned with development code 3
DEV_4 = 'dev4'  # acres assigned with development code 4
DEV_5 = 'dev5'  # acres assigned with development code 5
DEV_6 = 'dev6'  # acres assigned with development code 6
DEV_7 = 'dev7'  # acres assigned with development code 7
DEV_8 = 'dev8'  # acres assigned with development code 8
DEV_9 = 'dev9'  # acres assigned with development code 9
DEV_10 = 'dev10'  # acres assigned with development code 10
DEV_11 = 'dev11'  # acres assigned with development code 11
DEV_12 = 'dev12'  # acres assigned with development code 12
DEV_13 = 'dev13'  # acres assigned with development code 13
DEV_14 = 'dev14'  # acres assigned with development code 14
DEV_15 = 'dev15'  # acres assigned with development code 15
DEV_16 = 'dev16'  # acres assigned with development code 16
DWELLING_UNITS_PER_ACRE = 'dua'  # dwelling units per acre
HOUSING_CAPACITY = 'cap_hs'  # housing stock (dwelling unit) capacity
# housing stock (dwelling unit) capacity - single-family
SINGLE_FAMILY_HOUSING_CAPACITY = 'cap_hs_sf'
# housing stock (dwelling unit) capacity - multi-family
MULTI_FAMILY_HOUSING_CAPACITY = 'cap_hs_mf'
# housing stock (dwelling unit) capacity - mobile homes
MOBILE_HOME_HOUSING_CAPACITY = 'cap_hs_mh'
CIVILIAN_EMPLOYMENT_CAPACITY = 'cap_emp_civ'  # civilian employment capacity

# Parameter labels

# product types - must match parameter labels
SINGLE_FAMILY = 'single_family'
MULTI_FAMILY = 'multi_family'

INDUSTRIAL = 'industrial'
COMMERCIAL = 'commercial'
OFFICE = 'office'

# postfixes
MINIMUM_UNIT_SIZE_POSTFIX = '_minimum_unit_size'
JOB_AREA_POSTFIX = '_square_feet_per_job'
UNITS_PER_YEAR_POSTFIX = '_units_per_year'
CONSTRUCTION_COST_POSTFIX = '_construction_cost'


# TODO: add total units and occupied units data for non-residential when available
def development_constants(product_type):
    '''
        Returns developed land, vacant land, total units, and occupied units
        column labels for each product type
    '''
    if product_type == OFFICE:
        return OFFICE_DEVELOPED_ACRES, OFFICE_VACANT_ACRES, None, None
    elif product_type == COMMERCIAL:
        return COMMERCIAL_DEVELOPED_ACRES, COMMERCIAL_VACANT_ACRES, None, None
    elif product_type == INDUSTRIAL:
        return INDUSTRIAL_DEVELOPED_ACRES, INDUSTRIAL_VACANT_ACRES, None, None
    elif product_type == SINGLE_FAMILY:
        return SINGLE_FAMILY_DEVELOPED_ACRES, SINGLE_FAMILY_VACANT_ACRES, \
            SINGLE_FAMILY_HOUSING_UNITS, SINGLE_FAMILY_HOUSEHOLDS
    elif product_type == MULTI_FAMILY:
        return MULTI_FAMILY_DEVELOPED_ACRES, MULTI_FAMILY_VACANT_ACRES, \
            MULTI_FAMILY_HOUSING_UNITS, MULTI_FAMILY_HOUSEHOLDS


def product_type_price(product_type):
    '''
        Returns the column label for rents/prices
        for the product type argument
    '''
    if product_type == SINGLE_FAMILY:
        return SINGLE_FAMILY_RENT
    elif product_type == MULTI_FAMILY:
        return MULTI_FAMILY_RENT
    elif product_type == OFFICE:
        return OFFICE_RENT
    elif product_type == INDUSTRIAL:
        return INDUSTRIAL_RENT
    elif product_type == COMMERCIAL:
        return COMMERCIAL_RENT
