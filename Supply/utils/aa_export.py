# see FloorspaceO.csv for example output
'''
eg.
TAZ,Commodity,Quantity
16,Active Park Space,0
'''
# used PECAS_FloorspaceCommodities.csv for codes_labels

import pandas
import csv
from tqdm import tqdm

from utils.interface import save_to_file
from utils.constants import MGRA, INDUSTRIAL_TOTAL_SQUARE_FOOTAGE, \
    COMMERCIAL_TOTAL_SQUARE_FOOTAGE, OFFICE_TOTAL_SQUARE_FOOTAGE

CROSSWALK_ENTRY_COUNT = 368033

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


class SquareFootageCache(object):
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.cache = {}

    def __add(self, mgra_id, info):
        self.cache[mgra_id] = info

    def get_square_footages(self, mgra_id):
        if mgra_id in self.cache:
            return self.cache[mgra_id]
        else:
            info = get_mgra_info(self.dataframe, mgra_id, [
                INDUSTRIAL_TOTAL_SQUARE_FOOTAGE,
                OFFICE_TOTAL_SQUARE_FOOTAGE,
                COMMERCIAL_TOTAL_SQUARE_FOOTAGE
            ])
            self.__add(mgra_id, info)
            return info


def create_row(mgra_id, commodity, quantity):
    return {"MGRA": mgra_id,
            "Commodity": commodity,
            "Quantity": quantity}


# consider starting an access helper methods file with this included
def get_mgra_item(mgra_dataframe, mgra_id, column):
    return mgra_dataframe.loc[
        mgra_dataframe[MGRA] == mgra_id, column
    ].values.item()


def get_mgra_info(mgra_dataframe, mgra_id, columns):
    # returns a list containing the items in columns for the mgra specified by
    # mgra_id
    # ! only works if the mgras match the frame index - 1
    row = mgra_dataframe.loc[mgra_dataframe[MGRA] == mgra_id, columns]
    items = row.lookup([mgra_id-1] * len(columns), columns)
    return items


def calculate_quantity(cache, mgra_id, inputs):
    # if all ratios are zero return zero immediately
    industrial_ratio = float(inputs["IND"])
    commercial_ratio = float(inputs["COM"])
    office_ratio = float(inputs["OFC"])
    if industrial_ratio + commercial_ratio + office_ratio == 0.0:
        return 0
    # return sum of all quantities times the respective floorspace column in
    # the mgra
    square_footages = cache.get_square_footages(mgra_id)
    return int(
        industrial_ratio * square_footages[0] +
        office_ratio * square_footages[1] +
        commercial_ratio * square_footages[2]
    )


def export_aa(frame):
    cache = SquareFootageCache(frame)
    output_rows = []
    with open('data/CRE2FSC.csv') as f:
        dict_reader = csv.DictReader(f)
        # for each row in crosswalk; add row to output after finding quantity
        # and expanding commodity code
        # FIXME: it looks like the dict reader might be the reason for the
        # slowdown, as the cache now makes for only 23000 pandas operations
        with tqdm(total=CROSSWALK_ENTRY_COUNT) as progress:
            for row in dict_reader:
                mgra = int(row["MGRA"])
                commodity = codes_labels[int(row["FSC_num"])]
                quantity = calculate_quantity(cache, mgra, row)
                if quantity != 0:
                    output_rows.append(create_row(mgra, commodity, quantity))
                progress.update()

    output_frame = pandas.DataFrame(output_rows)
    save_to_file(output_frame, 'data/output', 'aa_export.csv')


if __name__ == "__main__":
    frame = pandas.read_csv('data/SRF_Input_Base_V4.1.csv')
    export_aa(frame)
