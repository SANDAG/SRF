import random

from utils.access_labels import all_product_type_labels


class DemandSatisfaction():
    def __init__(self, required_demand) -> None:
        self.required_demand = required_demand
        self.fulfilled_demand = 0
    
    def demand_unsatisfied(self):
        return self.fulfilled_demand < self.required_demand

    def finish(self):
        self.required_demand = self.fulfilled_demand

    def update(self, difference):
        self.fulfilled_demand += difference
    

class DemandManager():
    def __init__(self) -> None:
        self.labels_demands = {}
        for product_type_labels in all_product_type_labels():
            units_required = product_type_labels.units_per_year_parameter()
            if units_required < 0:
                units_required = 0
            self.labels_demands[product_type_labels] = DemandSatisfaction(units_required)

    def demands_unsatisfied(self):
        for demand in self.labels_demands.values():
            if demand.demand_unsatified():
                return True
        return False

    def sum_demand(self):
        total = 0
        for demand in self.labels_demands.values():
            total += demand.required_demand
        return total

    def random_order_items(self):
        items = list(self.labels_demands.items())
        return random.shuffle(items)

    def update_labels_demand(self, labels, difference):
        if difference is None:
            # we ran out of suitable candidates, stop trying to allocate by
            # setting demand to the amount built.
            self.labels_demands[labels].finish()
        else:
            self.labels_demands[labels].update(difference)

    def subtract_from_fulfilled_demand(self, product_type, removed_units):
        self.labels_demands[product_type].update(removed_units)

