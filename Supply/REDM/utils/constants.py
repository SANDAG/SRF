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
# Civilian group quarters population- other,
# for example senior housing, homeless pop.'
GROUP_QUARTERS_OTHER_POPULATION = 'gq_civ_other'
MILITARY_POPULATION = 'gq_mil'  # Military group quarters population

HOUSING_UNITS = 'hs'  # Housing units
SINGLE_FAMILY_HOUSING_UNITS = 'hs_sf'  # Single-family housing units
MULTI_FAMILY_HOUSING_UNITS = 'hs_mf'  # Multiple-family housing units
MOBILE_HOUSING_UNITS = 'hs_mh'  # Mobile home housing units
INDUSTRIAL_BUILDINGS = 'Ind_Ct'  # number of industrial buildings
COMMERCIAL_BUILDINGS = 'Ret_Ct'  # number of commercial/retail buildings
OFFICE_BUILDINGS = 'Ofc_Ct'  # number of office buildings

# total squarefootage of single-family units
SINGLE_FAMILY_TOTAL_SQUARE_FOOTAGE = 'SqFt_SF'
# total squarefootage of multiple-family units
MULTI_FAMILY_TOTAL_SQUARE_FOOTAGE = 'SqFt_MF'
# total square feet in industrial buildings
INDUSTRIAL_TOTAL_SQUARE_FOOTAGE = 'Ind_SqFt'
# total squarefeet in commercial/retail buildings
COMMERCIAL_TOTAL_SQUARE_FOOTAGE = 'Ret_SqFt'
# total squarefeet in office buildings
OFFICE_TOTAL_SQUARE_FOOTAGE = 'Ofc_SqFt'

HOUSEHOLDS = 'hh'  # Households (occupied housing units)
# Single-family households (occupied housing units)
SINGLE_FAMILY_HOUSEHOLDS = 'hh_sf'
# Multiple-family households (occupied housing units)
MULTI_FAMILY_HOUSEHOLDS = 'hh_mf'
MOBILE_HOUSEHOLDS = 'hh_mh'  # Mobile home households (occupied housing units)

# unused, hoping to remove in v 4.1
# occupied non-residential square-footages
INDUSTRIAL_OCCUPIED_UNITS = 'Occ_Indus'
OFFICE_OCCUPIED_UNITS = 'Occ_Offic'
COMMERCIAL_OCCUPIED_UNITS = 'Occ_Retl'
# unoccupied non-residential square-footages
INDUSTRIAL_VACANT_UNITS = 'Unoc_Indus'
COMMERCIAL_VACANT_UNITS = 'Unoc_Retl'
OFFICE_VACANT_UNITS = 'Unoc_Offic'

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

OFFICE_EMPLOYMENT = 'emp_office'
INDUSTRIAL_EMPLOYMENT = 'emp_indus_'
COMMERCIAL_EMPLOYMENT = 'emp_comm_l'
OTHER_EMPLOYMENT = 'emp_other_'
# acres developed as spaced rural residential; lot sizes of one acre or more
RURAL_DEVELOPED_ACRES = 'dev_ldsf'
# acres developed as single family residential; detached housing units on lots
# smaller than one acre
SINGLE_FAMILY_DEVELOPED_ACRES = 'dev_sf'
# acres developed as multiple family residential
MULTI_FAMILY_DEVELOPED_ACRES = 'dev_mf'
MOBILE_HOME_DEVELOPED_ACRES = 'dev_mh'  # acres developed as mobile home parks
# acres developed as group quarters residential
GROUP_QUARTERS_DEVELOPED_ACRES = 'dev_oth'
# acres developed as agricultural, extractive industry,
# or junkyard/dumps/landfills
AGRICULTURE_DEVELOPED_ACRES = 'dev_ag'
# acres developed as industrial, wholesale trade, airport, rail station,
# communications and utilities, center city parking, park and ride lots,
# other transportation, or marine terminals
INDUSTRIAL_DEVELOPED_ACRES = 'dev_indus'
# acres developed as retail trade, hotels/motels/resorts, public services,
# hospitals, or commercial recreation
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
# undeveloped acres planned for agricultural, extractive industry, or
# junkyard/dumps/landfills
AGRICULTURE_VACANT_ACRES = 'vac_ag'
# undeveloped acres planned for industrial, wholesale trade, airport,
# rail station, communications and utilities, center city parking, park and
# ride lots, other transportation, or marine terminals
INDUSTRIAL_VACANT_ACRES = 'vac_indus'
# undeveloped acres planned for retail trade, hotels/motels/resorts, public
# services, hospitals, or commercial recreation
COMMERCIAL_VACANT_ACRES = 'vac_comm'
OFFICE_VACANT_ACRES = 'vac_office'  # undeveloped acres planned for offices
SCHOOLS_VACANT_ACRES = 'vac_schools'  # undeveloped acres planned for schools
# undeveloped acres planned for freeways, railroads, or surface streets
ROADS_VACANT_ACRES = 'vac_roads'
# acres developed as single family residential, planned for redevelopment as
# multiple family residential
SINGLE_FAMILY_MULTI_FAMILY_REDEVELOPMENT_ACRES = 'redev_sf_m'
# acres developed as single family residential, planned for redevelopment as
# employment use
SINGLE_FAMILY_EMPLOYMENT_REDEVELOPMENT_ACRES = 'redev_sf_e'
# acres developed as multiple family residential, planned for redevelopment as
# employment use
MULTI_FAMILY_EMPLOYMENT_REDEVELOPMENT_ACRES = 'redev_mf_e'
# acres developed as mobile home parks, planned for redevelopment as single
# family residential
MOBILE_HOME_SINGLE_FAMILY_REDEVELOPMENT_ACRES = 'redev_mh_s'
# acres developed as mobile home parks, planned for redevelopment as multiple
# family residential
MOBILE_HOME_MULTI_FAMILY_REDEVELOPMENT_ACRES = 'redev_mh_m'
# acres developed as mobile home parks, planned for redevelopment as
# employment use
MOBILE_HOME_EMPLOYMENT_REDEVELOPMENT_ACRES = 'redev_mh_e'
# acres developed as agricultural, extractive industry,
# or junkyard/dumps/landfills planned for redevelopment as
# single family residential
AGRICULTURE_SINGLE_FAMILY_REDEVELOPMENT_ACRES = 'redev_ag_s'
# acres developed as agricultural, extractive industry, or
# junkyard/dumps/landfills planned for redevelopment as
# multiple family residential
AGRICULTURE_MULTI_FAMILY_REDEVELOPMENT_ACRES = 'redev_ag_m'
# acres developed as agricultural, extractive industry,
# or junkyard/dumps/landfills planned for redevelopment as industrial,
# wholesale trade, airport, rail station, communications and utilities,
# center city parking, park and ride lots, other transportation,
AGRICULTURE_INDUSTRIAL_REDEVELOPMENT_ACRES = 'redev_ag_i'
# acres developed as agricultural, extractive industry, or
# junkyard/dumps/landfills planned for redevelopment as retail trade,
# hotels/motels/resorts, public services, hospitals, or commercial recreation
AGRICULTURE_COMMERCIAL_REDEVELOPMENT_ACRES = 'redev_ag_c'
# acres developed as agricultural, extractive industry, or
# junkyard/dumps/landfills planned for redevelopment as offices
AGRICULTURE_OFFICE_REDEVELOPMENT_ACRES = 'redev_ag_o'
# acres developed as employment use, planned for redevelopment as
# residential
EMPLOYMENT_RESIDENTIAL_REDEVELOPMENT_ACRES = 'redev_emp1'
# acres developed as employment use, planned for redevelopment as a
# different category of employment use
EMPLOYMENT_EMPLOYMENT_REDEVELOPMENT_ACRES = 'redev_emp_'
# developed acres planned for single family residential infill
SINGLE_FAMILY_INFILL_ACRES = 'infill_sf'
# developed acres planned for multiple family residential infill
MULTI_FAMILY_INFILL_ACRES = 'infill_mf'
# developed acres planned for employment infill
EMPLOYMENT_INFILL_ACRES = 'infill_emp'
TOTAL_ACRES = 'acres'  # total acres
DEVELOPED_ACRES = 'dev'  # total developed acres
VACANT_ACRES = 'vac'  # total vacant acres
# vacant land not available for development for physical, public policy,
# or environmental reasons
UNUSABLE_ACRES = 'unusable'
LAND_COST_PER_ACRE = 'Land_Cost'  # cost of land per acre

# price/rent cost per square foot for single family dwelling
SINGLE_FAMILY_PRICE = 'Price_SF'
# price/rent cost per square foot for multi family dwelling
MULTI_FAMILY_PRICE = 'Price_MF'
# price/rent cost per square foot for commercial/retail building
COMMERCIAL_PRICE = 'Ret_Cost'
# price/rent cost per square foot for industrial building
INDUSTRIAL_PRICE = 'Ind_Cost'
# price/rent cost per square foot for office building
OFFICE_PRICE = 'Ofc_Cost'

DWELLING_UNITS_PER_ACRE = 'DUA'  # dwelling units per acre
HOUSING_CAPACITY = 'Cap_HS'  # housing stock (dwelling unit) capacity
# housing stock (dwelling unit) capacity - single-family
SINGLE_FAMILY_HOUSING_CAPACITY = 'Cap_HS_SF'
# housing stock (dwelling unit) capacity - multi-family
MULTI_FAMILY_HOUSING_CAPACITY = 'Cap_HS_MF'
# housing stock (dwelling unit) capacity - mobile homes
MOBILE_HOME_HOUSING_CAPACITY = 'Cap_HS_MH'
CIVILIAN_EMPLOYMENT_CAPACITY = 'cap_emp_civ'  # civilian employment capacity
SQFT_AREA = 'Shape_Area'

# interpolated columns from manhan group
SINGLE_FAMILY_MEAN_PRICE = "SF_mean"
MULTI_FAMILY_MEAN_PRICE = "MFmean"
INDUSTRIAL_MEAN_PRICE = "INDmean"
OFFICE_MEAN_PRICE = "OFCmean"
COMMERCIAL_MEAN_PRICE = "RETmean"

MULTI_FAMILY_PERCENT_OWNED = "mf_ownedme"
SINGLE_FAMILY_PERCENT_OWNED = "sf_ownedme"

INDUSTRIAL_JOB_AREA = "sf_indmean"
COMMERCIAL_JOB_AREA = "sf_commean"
OFFICE_JOB_AREA = "sf_ofcmean"

INDUSTRIAL_FAR = "far_indmea"
COMMERCIAL_FAR = "far_commea"
OFFICE_FAR = "far_ofcmea"

MULTI_FAMILY_PERCENT_NEW = "mf_new_mea"
MULTI_FAMILY_PERCENT_OLD = "mf_old_mea"
SINGLE_FAMILY_PERCENT_NEW = "sf_new_mea"
SINGLE_FAMILY_PERCENT_OLD = "sf_old_mea"
# "sfBedsmean", "mfBedsmean", "sfRoommean", "mfRoommean"

# added Job spaces column
OFFICE_JOB_SPACES = "office_js"
COMMERCIAL_JOB_SPACES = "commercial_js"
INDUSTRIAL_JOB_SPACES = "industrial_js"


REDM_IO_COLUMNS = [
    MGRA, SINGLE_FAMILY_TOTAL_SQUARE_FOOTAGE,
    MULTI_FAMILY_TOTAL_SQUARE_FOOTAGE, LAND_COST_PER_ACRE,
    SINGLE_FAMILY_MEAN_PRICE, MULTI_FAMILY_MEAN_PRICE, OFFICE_MEAN_PRICE,
    COMMERCIAL_MEAN_PRICE, INDUSTRIAL_MEAN_PRICE, HOUSING_UNITS,
    SINGLE_FAMILY_HOUSING_UNITS, MULTI_FAMILY_HOUSING_UNITS, HOUSEHOLDS,
    SINGLE_FAMILY_HOUSEHOLDS, MULTI_FAMILY_HOUSEHOLDS, INDUSTRIAL_EMPLOYMENT,
    COMMERCIAL_EMPLOYMENT, OFFICE_EMPLOYMENT, OTHER_EMPLOYMENT,
    INDUSTRIAL_JOB_AREA, COMMERCIAL_JOB_AREA, OFFICE_JOB_AREA, OFFICE_FAR,
    COMMERCIAL_FAR, INDUSTRIAL_FAR, SINGLE_FAMILY_DEVELOPED_ACRES,
    MULTI_FAMILY_DEVELOPED_ACRES, INDUSTRIAL_DEVELOPED_ACRES,
    COMMERCIAL_DEVELOPED_ACRES, OFFICE_DEVELOPED_ACRES,
    SINGLE_FAMILY_VACANT_ACRES, MULTI_FAMILY_VACANT_ACRES, OFFICE_VACANT_ACRES,
    COMMERCIAL_VACANT_ACRES, INDUSTRIAL_VACANT_ACRES, DEVELOPED_ACRES,
    VACANT_ACRES, UNUSABLE_ACRES, TOTAL_ACRES, DWELLING_UNITS_PER_ACRE,
    HOUSING_CAPACITY, SINGLE_FAMILY_HOUSING_CAPACITY,
    MULTI_FAMILY_HOUSING_CAPACITY, INDUSTRIAL_BUILDINGS,
    INDUSTRIAL_TOTAL_SQUARE_FOOTAGE, OFFICE_TOTAL_SQUARE_FOOTAGE,
    OFFICE_BUILDINGS, COMMERCIAL_TOTAL_SQUARE_FOOTAGE, COMMERCIAL_BUILDINGS,
    AGRICULTURE_COMMERCIAL_REDEVELOPMENT_ACRES,
    AGRICULTURE_INDUSTRIAL_REDEVELOPMENT_ACRES,
    AGRICULTURE_MULTI_FAMILY_REDEVELOPMENT_ACRES,
    AGRICULTURE_OFFICE_REDEVELOPMENT_ACRES,
    AGRICULTURE_SINGLE_FAMILY_REDEVELOPMENT_ACRES,
    EMPLOYMENT_EMPLOYMENT_REDEVELOPMENT_ACRES,
    EMPLOYMENT_RESIDENTIAL_REDEVELOPMENT_ACRES,
    MOBILE_HOME_EMPLOYMENT_REDEVELOPMENT_ACRES,
    MOBILE_HOME_MULTI_FAMILY_REDEVELOPMENT_ACRES,
    MOBILE_HOME_SINGLE_FAMILY_REDEVELOPMENT_ACRES,
    MULTI_FAMILY_EMPLOYMENT_REDEVELOPMENT_ACRES,
    SINGLE_FAMILY_EMPLOYMENT_REDEVELOPMENT_ACRES,
    SINGLE_FAMILY_MULTI_FAMILY_REDEVELOPMENT_ACRES, EMPLOYMENT_INFILL_ACRES,
    MULTI_FAMILY_INFILL_ACRES, SINGLE_FAMILY_INFILL_ACRES, OFFICE_JOB_SPACES,
    COMMERCIAL_JOB_SPACES, INDUSTRIAL_JOB_SPACES
]

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
AVERAGE_UNIT_SQFT_POSTFIX = '_average_sqft_per_unit'
AVERAGE_LAND_USAGE_PER_UNIT_POSTFIX = '_average_land_acres_per_unit'
JOB_SPACES_PER_BUILDING_POSTFIX = '_job_spaces_per_building'
MAX_VACANT_UNITS_POSTFIX = '_max_vacant_units'

# collections
OFFICE_LABELS = [
    OFFICE, OFFICE_EMPLOYMENT, OFFICE_DEVELOPED_ACRES, OFFICE_FAR,
    OFFICE_JOB_AREA, OFFICE_MEAN_PRICE, OFFICE_TOTAL_SQUARE_FOOTAGE,
    OFFICE_BUILDINGS, OFFICE_VACANT_UNITS
]

PRODUCT_TYPES = [
    SINGLE_FAMILY, MULTI_FAMILY, INDUSTRIAL, COMMERCIAL, OFFICE
]

NON_RESIDENTIAL_TYPES = [
    INDUSTRIAL, COMMERCIAL, OFFICE
]


class ProductTypeLabels(object):

    def __init__(self, product_type):
        super().__init__()
        self.product_type = product_type
        if self.product_type == SINGLE_FAMILY:
            self.occupied_units = SINGLE_FAMILY_HOUSEHOLDS
            self.total_units = SINGLE_FAMILY_HOUSING_UNITS
            self.square_footage = SINGLE_FAMILY_TOTAL_SQUARE_FOOTAGE
            self.developed_acres = SINGLE_FAMILY_DEVELOPED_ACRES
            self.vacant_acres = SINGLE_FAMILY_VACANT_ACRES
            self.price = SINGLE_FAMILY_MEAN_PRICE
        elif self.product_type == MULTI_FAMILY:
            self.occupied_units = MULTI_FAMILY_HOUSEHOLDS
            self.total_units = MULTI_FAMILY_HOUSING_UNITS
            self.square_footage = MULTI_FAMILY_TOTAL_SQUARE_FOOTAGE
            self.developed_acres = MULTI_FAMILY_DEVELOPED_ACRES
            self.vacant_acres = MULTI_FAMILY_VACANT_ACRES
            self.price = MULTI_FAMILY_MEAN_PRICE
        elif self.product_type == OFFICE:
            self.occupied_units = OFFICE_EMPLOYMENT
            self.total_units = OFFICE_JOB_SPACES
            self.square_footage = OFFICE_TOTAL_SQUARE_FOOTAGE
            self.developed_acres = OFFICE_DEVELOPED_ACRES
            self.vacant_acres = OFFICE_VACANT_ACRES
            self.price = OFFICE_MEAN_PRICE
            # non-residential specific
            self.buildings = OFFICE_BUILDINGS
            self.job_area = OFFICE_JOB_AREA
        elif self.product_type == COMMERCIAL:
            self.occupied_units = COMMERCIAL_EMPLOYMENT
            self.total_units = COMMERCIAL_JOB_SPACES
            self.square_footage = COMMERCIAL_TOTAL_SQUARE_FOOTAGE
            self.developed_acres = COMMERCIAL_DEVELOPED_ACRES
            self.vacant_acres = COMMERCIAL_VACANT_ACRES
            self.price = COMMERCIAL_MEAN_PRICE
            # non-residential specific
            self.buildings = COMMERCIAL_BUILDINGS
            self.job_area = COMMERCIAL_JOB_AREA
        elif self.product_type == INDUSTRIAL:
            self.occupied_units = INDUSTRIAL_EMPLOYMENT
            self.total_units = INDUSTRIAL_JOB_SPACES
            self.square_footage = INDUSTRIAL_TOTAL_SQUARE_FOOTAGE
            self.developed_acres = INDUSTRIAL_DEVELOPED_ACRES
            self.vacant_acres = INDUSTRIAL_VACANT_ACRES
            self.price = INDUSTRIAL_MEAN_PRICE
            # non-residential specific
            self.buildings = INDUSTRIAL_BUILDINGS
            self.job_area = INDUSTRIAL_JOB_AREA

    def is_residential(self):
        return self.product_type == SINGLE_FAMILY \
            or self.product_type == MULTI_FAMILY
