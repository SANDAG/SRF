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
    columns = mgra_labels.list_labels()

    for product_type in product_types():
        columns.extend(ProductTypeLabels(product_type).list_labels())
    return columns
