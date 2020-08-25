# see FloorspaceO.csv for example output
'''
eg.
LUZ,Commodity,Quantity
16,Active Park Space,0
'''
import os
import pandas
import csv

from utils.interface import save_to_file, extract_csv_from_database, parameters
from utils.access_labels import mgra_labels, ProductTypeLabels

CROSSWALK_FILENAME = 'aa_crosswalk.csv'

# used PECAS_FloorspaceCommodities.csv for codes_labels
codes_labels = {
    53: "Agriculture and Mining Space",
    54: "Light Industrial Space",
    55: "Heavy Industry Space",
    56: "Office Space",
    57: "Retail Space",
    58: "Depot Space",
    59: "Hotel Space",
    60: "Primary Schools",
    61: "Secondary Schools",
    62: "Post-Secondary Institution Space",
    63: "College Dormitory Space",
    64: "Health Care Space",
    65: "Religious Space",
    66: "Recreation Space",
    67: "Active Park Space",
    68: "Government Operations Space",
    69: "Dump Space",
    70: "Spaced Rural Residential Economy",
    71: "Spaced Rural Residential Luxury",
    72: "Single Family Detached Residential Economy",
    73: "Single Family Detached Residential Luxury",
    74: "Single Family Attached Residential Economy",
    75: "Single Family Attached Residential Luxury",
    76: "Multi-Family Residential Economy",
    77: "Multi-Family Residential Luxury",
    78: "Mobile Home Residential",
    79: "Military Residential(Non GQ)",
}


def create_row(luz, commodity, quantity):
    # needs to be labeled 'TAZ' for compatibility
    return {"TAZ": luz,
            "Commodity": commodity,
            "Quantity": quantity}


def calculate_quantity(square_footages, ratios):
    # return sum of all ratios times the respective floorspace column in
    # the mgra
    return int(
        ratios['industrial'] * square_footages[0] +
        ratios['commercial'] * square_footages[1] +
        ratios['office'] * square_footages[2]
    )


def luz_dict_from_crosswalk():
    result_dict = {}
    with open(os.path.join('data', CROSSWALK_FILENAME)) as f:
        reader = csv.DictReader(f)
        for row in reader:
            luz = int(row["LUZ"])
            commodity = codes_labels[int(row["FSC_num"])]
            ratios = {
                'industrial': float(row["IND"]),
                'commercial': float(row["COM"]),
                'office': float(row["OFC"]),
                'other': float(row["OTH"]),
            }
            if sum(ratios.values()) == 0.0:
                pass
            entry = {
                'commodity': commodity,
                'ratios': ratios
            }
            if luz not in result_dict:
                result_dict[luz] = [entry]
            else:
                result_dict[luz].append(entry)
    return result_dict


def export_luz_data(frame):
    extract_csv_from_database(
        parameters['schema'], parameters['aa_crosswalk_table'],
        'data', CROSSWALK_FILENAME)
    luz_dict = luz_dict_from_crosswalk()
    output_dict = {}
    focus_columns = [
        mgra_labels.LUZ,
        ProductTypeLabels('industrial').square_footage,
        ProductTypeLabels('commercial').square_footage,
        ProductTypeLabels('office').square_footage
    ]
    focus_frame = frame[focus_columns]
    # iterating through a pandas frame returns a python namedtuple
    for row in focus_frame.itertuples(index=False):  # for each mgra
        # use the namedtuple._asdict to access with the labels we are used to.
        row_dict = row._asdict()
        square_footages = [row_dict[focus_columns[1]],
                           row_dict[focus_columns[2]],
                           row_dict[focus_columns[3]]
                           ]
        if sum(square_footages) != 0:
            luz = row[0]  # find matching LUZ
            for commodity_info in luz_dict[luz]:  # check each commodity type
                commodity_name = commodity_info['commodity']
                ratios = commodity_info['ratios']
                quantity = calculate_quantity(square_footages, ratios)
                if quantity != 0:  # if there is some commodity space, add it.
                    # differentiate commodities for each luz with a tuple as a
                    # dict key
                    luz_commodity_tuple = (luz, commodity_name)
                    if luz_commodity_tuple not in output_dict:
                        output_dict[luz_commodity_tuple] = create_row(
                            luz, commodity_name, quantity)
                    else:
                        output_dict[
                            luz_commodity_tuple
                        ]['Quantity'] += quantity
    output_frame = pandas.DataFrame(output_dict.values())
    output_frame.sort_values(by=['Commodity', 'TAZ'], inplace=True)
    save_to_file(output_frame, 'data/output', 'aa_export.csv')


if __name__ == "__main__":
    frame = pandas.read_csv('data/SRF_Input_Base_V4.1.csv')
    export_luz_data(frame)
