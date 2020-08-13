import logging
import pandas
from tqdm import tqdm

import utils.config as config
from utils.interface import load_parameters, empty_folder, save_to_file, \
    open_dbf
from modeling.dataframe_updates import update_mgra
from utils.constants import ProductTypeLabels, SINGLE_FAMILY, \
    MULTI_FAMILY, MGRA, INDUSTRIAL_JOB_SPACES, COMMERCIAL_JOB_SPACES, \
    OFFICE_JOB_SPACES, INDUSTRIAL, COMMERCIAL, OFFICE, UNITS_PER_YEAR


def reduce_demand(product_type, units):
    config.parameters[UNITS_PER_YEAR][product_type] -= units


def add_to_mgra(mgras, site):
    '''
        mgras: the dataframe to update.
        site: expects a dataframe with one entry, including columns for MGRAID
        and the number of units to add
    '''
    mgra_id = site.MGRA.item()
    single_family_units = site.sfu.item()
    multi_family_units = site.mfu.item()
    employment_units = site.civEmp.item()

    if single_family_units > 0:
        # add single family units
        labels = ProductTypeLabels(SINGLE_FAMILY)
        update_mgra(
            mgras, mgra_id, single_family_units, labels)
        reduce_demand(labels.product_type, single_family_units)
    if multi_family_units > 0:
        # add multifamily units
        labels = ProductTypeLabels(MULTI_FAMILY)
        update_mgra(
            mgras, mgra_id, multi_family_units, labels)
        reduce_demand(labels.product_type, multi_family_units)
    if employment_units > 0:
        # add employment; determine which type to add
        mgra = mgras.loc[mgras[MGRA] == mgra_id, [
            INDUSTRIAL_JOB_SPACES, COMMERCIAL_JOB_SPACES, OFFICE_JOB_SPACES]]
        if mgra[INDUSTRIAL_JOB_SPACES].item() > 0:
            labels = ProductTypeLabels(INDUSTRIAL)
            update_mgra(mgras, mgra_id, employment_units, labels)
        elif mgra[COMMERCIAL_JOB_SPACES].item() > 0:
            labels = ProductTypeLabels(COMMERCIAL)
            update_mgra(mgras, mgra_id, employment_units, labels)
        elif mgra[OFFICE_JOB_SPACES].item() > 0:
            labels = ProductTypeLabels(OFFICE)
            update_mgra(mgras, mgra_id, employment_units, labels)
        else:  # we have to guess the product type... commercial seems likely!
            labels = ProductTypeLabels(COMMERCIAL)
            update_mgra(mgras, mgra_id, employment_units, labels)
        reduce_demand(labels.product_type, employment_units)

    return


def distribute_units(mgras, sites):
    '''
        mgras: the dataframe to update.
        sites: a dataframe with multiple entries, several mgras should be
        updated after splitting up the units
    '''
    areas = sites.Shape_Area
    total_area = areas.sum()
    area_per_site = areas / total_area
    # for each unit type
    labels = ['sfu', 'mfu', 'civEmp']
    for label in labels:
        # find total units
        total_units = sites.iloc[[0]][label].item()
        # reassign totals to match the area of the intersection
        sites.loc[:, label] = round(area_per_site * sites[label])

        # add or subtract missing units lost due to rounding
        sum_units = sites[label].sum()
        diff = total_units - sum_units
        if diff != 0:
            # find the largest area and add missing units to it
            # (or subtract if diff is negative)
            # there are no sites where this applies in the 2013 data, but this
            # is susceptible to an edge case where if more than one site had
            # the same units, they will both be added to.
            sites.loc[sites[label] == sites[label].max(), label] += diff
        diff = total_units - sites[label].sum()
        # ensure that edge case didn't happen
        if diff != 0:
            print(diff)
            print(sites)
            print(sites.mfu)
            print(total_units)
            assert diff == 0

    for i in range(len(sites)):
        add_to_mgra(mgras, sites.iloc[[i]])
    return


def find_sites(intersections, id):
    return intersections[intersections['siteid'] == id].copy()


def remove_other_years(intersections, starting_year):
    return intersections[intersections['phase'] == starting_year].copy()


def run(mgras, intersections, output_dir, progress=None, starting_year=None):
    if starting_year is not None:
        intersections = remove_other_years(intersections, starting_year)

    if len(intersections) == 0:
        print('no scheduled development found for year {}'
              .format(starting_year))
        return
    # add each site. we actually have a frame of intersections

    # find max siteID
    # for i = 1 through max_siteID
    # return instances of siteID in intersections
    # if there are none, skip
    # if there is one, put all development on the mgra
    # if there are multiple determine split.
    sites = []
    max_siteID = intersections.siteid.max()
    progress_bar = tqdm(range(max_siteID))
    progress_bar.set_description("splitting sites on mgras")
    for i in progress_bar:
        sites.append(find_sites(intersections, i + 1))

    # sites is a list of dataframes.

    progress_bar = tqdm(sites)
    progress_bar.set_description('allocating development for each site')
    for frame in progress_bar:
        if len(frame) == 0:
            pass
        elif len(frame) == 1:
            add_to_mgra(mgras, frame)
        else:
            distribute_units(mgras, frame)

    save_to_file(mgras, output_dir, 'planned_development_added.csv')
    return


if __name__ == "__main__":
    # load parameters
    config.parameters = load_parameters('parameters.yaml')

    if config.parameters is not None:
        # prep output directory
        output_dir = config.parameters['output_directory']
        empty_folder(output_dir)
        save_to_file(config.parameters, output_dir, 'parameters.txt')
        # configure logging level
        if config.parameters['debug']:
            logging.basicConfig(level=logging.DEBUG)
        # load dataframes
        mgra_dataframe = pandas.read_csv(config.parameters['input_filename'])
        input_sites = open_dbf(config.parameters['sites_filename'])

        run(mgra_dataframe, input_sites, output_dir)
    else:
        print('could not load parameters, exiting')
