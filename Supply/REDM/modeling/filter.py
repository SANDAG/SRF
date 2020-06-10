from numpy import floor
import pandas


def filter_mgras(mgras):
    filtered = mgras
    # filtered = filter_by_vacancy(filtered, vacancy_rate)
    # filtered = filter_redevelopment(
    #     filtered, forecast_year, minimum_redevelopment_age)
    # filtered = filter_by_profitability(filtered)
    return filtered


def filter_by_profitability(parcels_dataframe):
    costLand = parcels_dataframe.land_cost
    costConstruction = parcels_dataframe.construction_cost
    costRedevelopment = parcels_dataframe.redevelopment_cost
    profitMultiplier = 0.25
    minimumRevenue = ((costConstruction + costLand + costRedevelopment) *
                      profitMultiplier) + (costConstruction + costLand +
                                           costRedevelopment)
    indexLoc = parcels_dataframe[parcels_dataframe['expected_revenue']
                                 < minimumRevenue].index
    parcels_dataframe = parcels_dataframe.drop(indexLoc)
    return parcels_dataframe


def filter_by_vacancy(mgra_dataframe,
                      total_units_column, occupied_units_column,
                      target_vacancy_rate):
    # # step one: determine vacancy rate and add as another column of mgra csv
    # mgra_dataframe['vacancy_rate'] = (
    #     mgra_dataframe['hs'] - mgra_dataframe['hh']) / mgra_dataframe['hs']
    # # step two: drop mgras with vacancy rate greater than target_vacancy_rate
    # indexMGRA = mgra_dataframe[mgra_dataframe['vacancy_rate']
    #                            > target_vacancy_rate].index
    # mgra_dataframe = mgra_dataframe.drop(indexMGRA)
    # mgra_dataframe.drop(columns=['vacancy_rate'])

    max_new_units = max_new_units_to_meet_vacancy(
        mgra_dataframe, total_units_column, occupied_units_column,
        target_vacancy_rate
    )
    # We may want to use a number larger than zero
    filtered = mgra_dataframe[max_new_units > 0]

    # also return max_new_units to possibly use for weighting
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


def filter_redevelopment(parcels_dataframe, forecast_year, min_age):
    target_year = (forecast_year - min_age)
    indexParcels = parcels_dataframe[parcels_dataframe['year_built']
                                     >= target_year].index
    parcels_dataframe = parcels_dataframe.drop(indexParcels)
    return parcels_dataframe
