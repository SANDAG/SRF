

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


def filter_by_vacancy(parcels_dataframe, target_vacancy_rate):
    indexNames = parcels_dataframe[parcels_dataframe['vacancy_rate']
                                   > target_vacancy_rate].index
    parcels_dataframe = parcels_dataframe.drop(indexNames)
    return parcels_dataframe


def filter_redevelopment(parcels_dataframe, forecast_year, min_age):
    target_year = (forecast_year - min_age)
    indexParcels = parcels_dataframe[parcels_dataframe['year_built']
                                     >= target_year].index
    parcels_dataframe = parcels_dataframe.drop(indexParcels)
    return parcels_dataframe
