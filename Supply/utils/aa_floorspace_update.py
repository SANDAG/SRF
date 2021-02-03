# This takes an aa floorspace compatible, luz oriented file and adds any
# updates that are found in a supply compatible mgra based input/output file

# implemenation brainstorming:
# the aa_luz_export.py code already creates most of the expected output in the
# correct format. it could be easiest to run aa_luz_export, followed by some
# code here that consolidates the floorspaceI file and the output from
# aa_luz_export.
import os
import pandas

from utils.aa_luz_export import export_luz_data, create_row
from utils.interface import save_to_file
from utils.access_labels import ProductTypeLabels, mgra_labels


single_family_subtypes = [
    "Spaced Rural Residential Economy",
    "Spaced Rural Residential Luxury",
    "Single Family Detached Residential Economy",
    "Single Family Detached Residential Luxury",
    "Single Family Attached Residential Economy",
    "Single Family Attached Residential Luxury",
    # these two might need to get disabled if not applicable
    "Mobile Home Residential",
    "Military Residential(Non GQ)",
]
multi_family_subtypes = [
    "Multi-Family Residential Economy",
    "Multi-Family Residential Luxury",
]


def combine_frames(a, b):
    # combines two pandas frames containing aa floorspace input data
    # keeping the max quantity for each taz and commodity pair
    combined = pandas.merge(a, b, how='outer', on=['TAZ', 'Commodity'])
    combined['Quantity'] = combined[['Quantity_x', 'Quantity_y']].max(axis=1)
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


def add_floorspace_entry(entry, ratios, output):
    luz = entry[0]
    total_squarefootage = entry[1]
    if luz not in ratios:
        # there is no previous allocation of subtypes available, use the
        # average distribution from the region?
        # reaching this point too often would probably be an indicator of inaccurate behavior.
        return
    luz_ratios = ratios[luz]
    type_total = sum(luz_ratios.values())
    for subtype in luz_ratios.items():
        commodity = subtype[0]
        quantity = subtype[1]
        output.append(create_row(
            luz, commodity, total_squarefootage * (quantity / type_total)))


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
        add_floorspace_entry(entry, luz_ratios, output)


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
        floorspace_frame = combine_frames(floorspace_frame, supply_exports)
    else:
        print('could not find aa floorspaceI file.')
        print('continuing with non-residential export, ')
        print('aa may bog down on the missing data.')
        floorspace_frame = export_luz_data(mgra_frame)

    save_to_file(floorspace_frame, floorspace_directory,
                 floorspace_filename, force=True)
    return
