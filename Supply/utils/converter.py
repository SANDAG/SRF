SQUARE_FEET_PER_ACRE = 43560


def square_feet_to_acres(square_feet):
    return square_feet / SQUARE_FEET_PER_ACRE


def x_per_acre_to_x_per_square_foot(x):
    return x / SQUARE_FEET_PER_ACRE
