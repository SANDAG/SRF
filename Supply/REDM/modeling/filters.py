from numpy import floor
import pandas

import utils.config as config


def filter_product_type(mgra, product_type_vacant_key, acreage_per_unit):
    # must have space available
    return mgra[mgra[product_type_vacant_key] > acreage_per_unit * 1.2]


def filter_by_vacancy(mgra_dataframe,
                      total_units_column, occupied_units_column):

    target_vacancy_rate = config.parameters['target_vacancy_rate']

    max_new_units = max_new_units_to_meet_vacancy(
        mgra_dataframe, total_units_column, occupied_units_column,
        target_vacancy_rate
    )
    # return the MGRA's that can add more units to meet the target vacancy rate
    # We may want to use a number larger than zero
    filtered = mgra_dataframe[max_new_units > 0]

    # also return max_new_units to use for weighting
    return filtered, max_new_units


def max_new_units_to_meet_vacancy(mgra, total_units_column,
                                  occupied_units_column, target_vacancy_rate):
    # can be below zero if mgra is already over target vacancy rate
    # since vacancy = (total_units - occupied_units) / total_units
    # find max_units for a target_vacancy with some algebra:
    # max_units = -(occupied/(target_vacancy - 1))
    max_units = floor(
        -1*((mgra[occupied_units_column]) / (target_vacancy_rate - 1))
    )
    max_new_units = max_units - mgra[total_units_column]

    return max_new_units


# early brainstorming reference
# def filter_by_profitability(parcels_dataframe):
#     costLand = parcels_dataframe.land_cost
#     costConstruction = parcels_dataframe.construction_cost
#     costRedevelopment = parcels_dataframe.redevelopment_cost
#     profitMultiplier = 0.25
#     minimumRevenue = ((costConstruction + costLand + costRedevelopment) *
#                       profitMultiplier) + (costConstruction + costLand +
#                                            costRedevelopment)
#     indexLoc = parcels_dataframe[parcels_dataframe['expected_revenue']
#                                  < minimumRevenue].index
#     parcels_dataframe = parcels_dataframe.drop(indexLoc)
#     return parcels_dataframe
def filter_by_profitability(mgra_dataframe, product_type):
    pass

# Brainstorming reference
# def filter_redevelopment(parcels_dataframe, forecast_year, min_age):
#     target_year = (forecast_year - min_age)
#     indexParcels = parcels_dataframe[parcels_dataframe['year_built']
#                                      >= target_year].index
#     parcels_dataframe = parcels_dataframe.drop(indexParcels)
#     return parcels_dataframe
