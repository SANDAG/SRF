import collections
from utils.interface import load_yaml, parameters

# parameter names
UNITS_PER_YEAR = 'units_per_year'
CONSTRUCTION_COST = 'construction_cost'
UNIT_SQFT = 'sqft_per_unit'
LAND_USAGE_PER_UNIT = 'land_acres_per_unit'
JOB_SPACES_PER_BUILDING = 'job_spaces_per_building'
MAX_VACANT_UNITS = 'max_vacant_units'
TARGET_VACANCY_RATE = 'target_vacancy_rates'


def open_labels():
    return load_yaml('labels.yaml')


labels_dict = open_labels()
residential_types = labels_dict['product_types']['residential']
non_residential_types = labels_dict['product_types']['non_residential']


class MGRALabels(object):
    def __init__(self):
        super().__init__()
        self.MGRA = labels_dict['MGRA']
        self.LUZ = labels_dict['LUZ']
        self.TOTAL_ACRES = labels_dict["TOTAL_ACRES"]
        self.DEVELOPED_ACRES = labels_dict["DEVELOPED_ACRES"]
        self.VACANT_ACRES = labels_dict["VACANT_ACRES"]
        self.LAND_COST_PER_ACRE = labels_dict["LAND_COST_PER_ACRE"]
        self.HOUSING_UNITS = labels_dict["HOUSING_UNITS"]
        self.HOUSEHOLDS = labels_dict["HOUSEHOLDS"]
        self.TOTAL_JOB_SPACES = labels_dict["TOTAL_JOB_SPACES"]
        self.EMPLOYMENT = labels_dict["EMPLOYMENT"]
        self.HOUSING_CAPACITY = labels_dict["HOUSING_CAPACITY"]
        self.DWELLING_UNITS_PER_ACRE = labels_dict["DWELLING_UNITS_PER_ACRE"]
        self.CIVILIAN_EMPLOYMENT_CAPACITY = labels_dict[
            "CIVILIAN_EMPLOYMENT_CAPACITY"
        ]
        self.SHAPE_AREA = labels_dict["SHAPE_AREA"]

    def list_labels(self):
        return [
            self.MGRA, self.LUZ, self.TOTAL_ACRES, self.DEVELOPED_ACRES,
            self.VACANT_ACRES, self.LAND_COST_PER_ACRE, self.HOUSING_UNITS,
            self.HOUSEHOLDS, self.TOTAL_JOB_SPACES, self.EMPLOYMENT,
            self.HOUSING_CAPACITY, self.DWELLING_UNITS_PER_ACRE,
            self.CIVILIAN_EMPLOYMENT_CAPACITY
        ]


mgra_labels = MGRALabels()


def product_types():
    keys_list = list(residential_types.keys())
    keys_list.extend(list(non_residential_types.keys()))
    return keys_list


class ProductTypeLabels(object):
    def __init__(self, product_type=product_types()[0]):
        super().__init__()
        self.product_type = product_type
        self.residential = product_type in residential_types
        if self.residential:
            product_type_dict = residential_types[product_type]
            self.occupied_units = product_type_dict['HOUSEHOLDS']
            self.total_units = product_type_dict['HOUSING_UNITS']
            self.capacity = product_type_dict['HOUSING_CAPACITY']
        else:
            product_type_dict = non_residential_types[product_type]
            self.occupied_units = product_type_dict['EMPLOYMENT']
            self.total_units = product_type_dict['JOB_SPACES']
            self.job_area = product_type_dict['JOB_AREA']

        self.square_footage = product_type_dict['TOTAL_SQUARE_FOOTAGE']
        self.developed_acres = product_type_dict['DEVELOPED_ACRES']
        self.vacant_acres = product_type_dict['VACANT_ACRES']
        self.price = product_type_dict['MEAN_PRICE']

    def list_labels(self):
        result = [self.occupied_units, self.total_units, self.square_footage,
                  self.developed_acres, self.vacant_acres, self.price
                  ]
        if self.residential:
            result.append(self.capacity)
        else:
            result.append(self.job_area)
        return result

    def is_residential(self):
        return self.residential

    def construction_cost_parameter(self):
        return self.__param_from_dict(CONSTRUCTION_COST)

    def units_per_year_parameter(self):
        return self.__param_from_dict(UNITS_PER_YEAR)

    def unit_sqft_parameter(self):
        return self.__param_from_dict(UNIT_SQFT)

    def land_use_per_unit_parameter(self):
        return self.__param_from_dict(LAND_USAGE_PER_UNIT)

    def job_spaces_per_building_parameter(self):
        return self.__param_from_dict(JOB_SPACES_PER_BUILDING)

    def max_vacant_units_parameter(self):
        return self.__param_from_dict(MAX_VACANT_UNITS)

    def target_vacancy_rate_parameter(self):
        return self.__param_from_dict(TARGET_VACANCY_RATE)

    def __param_from_dict(self, param_name):
        return parameters[param_name][self.product_type]


def all_product_type_labels():
    labels_list = []
    for product_type in product_types():
        labels_list.append(ProductTypeLabels(product_type))
    return labels_list


class RedevelopmentLabels(object):
    def __init__(self):
        super().__init__()
        self.redevelopment_dict = labels_dict['redevelopment']
        self.multi_family = self.redevelopment_dict['multi_family'].values()
        self.employment = self.redevelopment_dict['employment'].values()
        self.single_family = self.redevelopment_dict['single_family'].values()
        self.industrial = self.redevelopment_dict['industrial'].values()
        self.commercial = self.redevelopment_dict['commercial'].values()
        self.office = self.redevelopment_dict['office'].values()
        self.residential = self.redevelopment_dict['residential'].values()
        self.infill_dict = labels_dict['infill']
        self.infill = labels_dict['infill'].values()

    def list_labels(self):
        result = []
        result.extend(self.multi_family)
        result.extend(self.employment)
        result.extend(self.single_family)
        result.extend(self.industrial)
        result.extend(self.commercial)
        result.extend(self.office)
        result.extend(self.residential)
        result.extend(self.infill)
        return result

    def applicable_labels_for(self, product_type_labels):
        # this returns all of the labels for land that could be used to
        # develop the product_type argument
        # product type must match redev dict entry labels

        labels = list(self.redev_labels(product_type_labels))

        infill_label = self.infill_label(product_type_labels)
        if infill_label is not None:
            labels.append(infill_label)

        labels.append(product_type_labels.vacant_acres)
        return labels

    def redev_labels(self, product_type_labels):
        labels = list(getattr(self, product_type_labels.product_type))
        if product_type_labels.residential:
            labels.extend(self.residential)
        else:  # employment, add redev
            labels.extend(self.employment)
        return labels

    def infill_label(self, product_type_labels):
        product_type = product_type_labels.product_type
        # there is only ever one
        label = None
        if product_type == 'single_family':
            label = self.infill_dict['SINGLE_FAMILY_INFILL_ACRES']
        elif product_type == 'multi_family':
            label = self.infill_dict['MULTI_FAMILY_INFILL_ACRES']
        elif not product_type_labels.residential:
            label = self.infill_dict['EMPLOYMENT_INFILL_ACRES']
        return label

    def label_type(self, label):
        LandType = collections.namedtuple(
            'LandType',
            ['infill', 'redev', 'vacant']
        )
        land_type = LandType(False, False, False)
        if label in self.infill:
            land_type = LandType(True, False, False)
        elif label in self.list_labels():
            land_type = LandType(False, True, False)
        else:
            land_type = LandType(False, False, True)
        return land_type

    def get_origin(self, label):
        '''
        returns the label corresponding to the original land use
        type for the redevelopment `label` argument
        '''
        # just do it by hand
        # single family origins
        if label == "redev_sf_m" or label == "redev_sf_e":
            return ProductTypeLabels('single_family')

        # mobile home origins # ! we don't have all info for mh available now
        # if "mh" in label:
        #     return "dev_mh"
        # agriculture origins
        # if "ag" in label:
        #     # ! would need to re-add this column to tables in the db :\
        #     return 'dev_ag'
        # multi family origins
        if label == "redev_mf_e":
            return ProductTypeLabels('multi_family')
        # employment origins
        if "emp" in label:
            # ! Pick a product type randomly?
            return ProductTypeLabels('commercial')

        return None


land_origin_labels = RedevelopmentLabels()


def increasing_columns():
    increasing_columns = []
    # add general labels
    increasing_columns.extend([
        labels_dict['DEVELOPED_ACRES'],
        labels_dict['HOUSING_UNITS'],
        labels_dict['TOTAL_JOB_SPACES'],
    ])
    # add labels for all product types
    for product_type in residential_types.values():
        increasing_columns.extend([
            product_type['HOUSING_UNITS'],
            product_type['TOTAL_SQUARE_FOOTAGE'],
            product_type['DEVELOPED_ACRES'],
        ])
    for product_type in non_residential_types.values():
        increasing_columns.extend([
            product_type['JOB_SPACES'],
            product_type['TOTAL_SQUARE_FOOTAGE'],
            product_type['DEVELOPED_ACRES'],
        ])
    return increasing_columns


def decreasing_columns():
    decreasing_columns = []
    labels_dict = open_labels()
    decreasing_columns.append(labels_dict['VACANT_ACRES'])
    for product_type in residential_types.values():
        decreasing_columns.append(product_type['VACANT_ACRES'])
    for product_type in non_residential_types.values():
        decreasing_columns.append(product_type['VACANT_ACRES'])
    return decreasing_columns


def all_columns():
    # need a list of all column labels used
    # start with general labels
    columns = mgra_labels.list_labels()
    # add all product types
    for product_type in product_types():
        columns.extend(ProductTypeLabels(product_type).list_labels())
    # also add redevelopment and infill
    columns.extend(RedevelopmentLabels().list_labels())

    # manually keeping other, agriculture, mh acres etc.
    columns.extend([
        'hs_mh', 'hh_mh', 'dev_mh', 'vac_mh', 'Cap_HS_MH',
        'emp_other_', 'dev_oth', 'vac_oth',
        'dev_ag', 'vac_ag'
    ])
    return columns
