# This takes an aa floorspace compatible, luz oriented file and adds any
# updates that are found in a supply compatible mgra based input/output file

import os
import pandas

from utils.aa_luz_export import export_luz_data, create_row
from utils.interface import save_to_file
from utils.access_labels import ProductTypeLabels, mgra_labels


single_family_subtypes = {
    "Spaced Rural Residential Economy": 0.06252183481,
    "Spaced Rural Residential Luxury": 0.02702450363,
    "Single Family Detached Residential Economy": 0.5718136716,
    "Single Family Detached Residential Luxury": 0.1953280044,
    "Single Family Attached Residential Economy": 0.1040184543,
    "Single Family Attached Residential Luxury": 0.03929353122,
}
multi_family_subtypes = {
    "Multi-Family Residential Economy": 0.656242618932389,
    "Multi-Family Residential Luxury": 0.221331960648503,
    "Mobile Home Residential": 0.122425420419106,
}


def combine_frames(a, b):
    # combines two pandas frames containing aa floorspace input data
    # keeps all non-duplicates (unique TAZ and commodity) from each frame
    # for duplicates: keeps the entry from a and ignores the entry from b
    if len(a) == 0:
        return b
    elif len(b) == 0:
        return a
    else:
        combined = pandas.merge(a, b, how='outer', on=['TAZ', 'Commodity'])
        combined['Quantity'] = combined['Quantity_x'].fillna(
            combined['Quantity_y'])
        combined = combined[['TAZ', 'Commodity', 'Quantity']]
        return combined


def luz_squarefootages(frame, product_squarefootage_label):
    luz_sqft = {}
    for row in frame.itertuples(index=False):
        row = row._asdict()
        if row['LUZ'] not in luz_sqft:
            luz_sqft[row['LUZ']] = row[product_squarefootage_label]
        else:
            luz_sqft[row['LUZ']] += row[product_squarefootage_label]
    return luz_sqft


def luz_subtype_ratios(floorspace, subtypes):
    luz_ratios = {}
    for row in floorspace.itertuples(index=False):
        row = row._asdict()
        if row['Commodity'] in subtypes:
            if row['TAZ'] not in luz_ratios:
                luz_ratios[row['TAZ']] = {row['Commodity']: row['Quantity']}
            else:
                luz_ratios[row['TAZ']][row['Commodity']] = row['Quantity']
    return luz_ratios


def add_floorspace_entry(entry, ratios, output, subtypes):
    luz = entry[0]
    total_squarefootage = entry[1]
    if total_squarefootage == 0:
        return
    if luz in ratios:
        luz_ratios = ratios[luz]
        type_total = sum(luz_ratios.values())
        if type_total > 0:
            for subtype in luz_ratios.items():
                commodity = subtype[0]
                quantity = subtype[1]
                output.append(create_row(
                    luz, commodity,
                    total_squarefootage * (quantity / type_total)
                ))
            return
    # there is no previous allocation of subtypes available, use the
    # average distribution from the region.
    for subtype in subtypes.items():
        output.append(create_row(
            luz, subtype[0], total_squarefootage * subtype[1]))
    return


def floorspace_for_product_type(
        output, mgra_frame, floorspace_input, product_type_label, subtypes):
    # find the sum of squarefootages on every luz
    square_footages = luz_squarefootages(mgra_frame, product_type_label)
    # find the ratio of each subtype for each luz on the input floorspace
    # frame, if it is available
    luz_ratios = luz_subtype_ratios(floorspace_input, subtypes)
    # allocate the sqft from the mgra_frame to the subtypes based on the
    # ratios for each luz
    for entry in square_footages.items():
        add_floorspace_entry(entry, luz_ratios, output, subtypes)


def calculate_residential_floorspace(mgra_frame, floorspace_input):
    # just look at the applicable fields
    single_family_sqft_label = ProductTypeLabels(
        'single_family').square_footage
    multi_family_sqft_label = ProductTypeLabels('multi_family').square_footage
    focus_columns = [
        mgra_labels.LUZ,
        single_family_sqft_label,
        multi_family_sqft_label,
    ]
    focus_frame = mgra_frame[focus_columns]
    # for both single family and multifamily
    output = []
    # add floorspace entries to the output
    floorspace_for_product_type(
        output, focus_frame, floorspace_input,
        single_family_sqft_label, single_family_subtypes)
    floorspace_for_product_type(
        output, focus_frame, floorspace_input,
        multi_family_sqft_label, multi_family_subtypes)

    return pandas.DataFrame(output)


def update_floorspace(mgra_frame, forecast_year):
    # get the original input frame and add to it if it exists
    floorspace_directory = '../PECAS/S28_aa/{}'.format(forecast_year)
    floorspace_filename = 'FloorspaceI.csv'
    floorspace_path = os.path.join(floorspace_directory, floorspace_filename)
    if os.path.isfile(floorspace_path):
        floorspace_frame = pandas.read_csv(floorspace_path)
        supply_exports = combine_frames(
            export_luz_data(mgra_frame),  # this is the non-residential data
            calculate_residential_floorspace(mgra_frame, floorspace_frame)
        )
        floorspace_frame = combine_frames(supply_exports, floorspace_frame)
    else:
        print('could not find aa floorspaceI file.')
        print('continuing with non-residential export, ')
        print('aa may bog down on the missing data.')
        floorspace_frame = export_luz_data(mgra_frame)

    save_to_file(floorspace_frame, 'data/output',
                 floorspace_filename, force=True)
    return
