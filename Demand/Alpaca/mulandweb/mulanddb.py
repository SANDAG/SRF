# coding: utf-8
# pylint: disable=invalid-name,bad-continuation,line-too-long
'''Implements MulandWeb\'s database access interfaces'''

import csv
from itertools import zip_longest

import shapefile
from sqlalchemy import select, func, and_, text
from shapely.geometry import Polygon

from .muland import MulandData
from . import db


__all__ = ['MulandDB', 'MulandDBException', 'ModelNotFound', 'ModelImporter']

class MulandDBException(Exception):
    '''Base Exception class for MulandDB'''
    pass
class ModelNotFound(MulandDBException):
    '''Model was not found at the database'''
    pass

class MulandDB:
    '''Provides data retrival from Muland Database'''
    # pylint: disable=too-few-public-methods
    def __init__(self, model: str, locations: list):
        '''Initialize class'''
        assert isinstance(model, str)

        self.conn = db.engine.connect()

        s = select([db.models.c.id]).where(db.models.c.name == model)
        result = self.conn.execute(s)
        row = result.fetchone()
        result.close()
        if result is None:
            raise ModelNotFound

        _units = []
        _locations = []
        for loc in locations:
            assert isinstance(loc['lnglat'][0], (int, float))
            assert isinstance(loc['lnglat'][1], (int, float))

            loc_overrides = {key: value for key, value in loc.items()
                             if key not in ['lnglat', 'units']}
            _location = {'location_id': len(_locations),
                         'lng': loc['lnglat'][0],
                         'lat': loc['lnglat'][1],
                         'overrides': loc_overrides}
            _locations.append(_location)

            for unit in loc['units']:
                unit_overrides = {key: value for key, value in unit.items()
                                  if key not in ['type']}
                _unit = {'unit_id': len(_units),
                         'location': _location,
                         'types_id': unit['type'],
                         'overrides': unit_overrides}
                _units.append(_unit)

        self.models_id = row[0]
        self.units = _units
        self.locations = _locations

    def _apply_overrides(self, data):
        '''Override data from db with values provided by user'''
        header = data.header
        if 'I_IDX' not in header and 'V_IDX' not in header:
            return

        records = data.records
        header_idx = {key.upper(): index
                      for key, index in zip(header, range(len(header)))}

        # if there is no type, iterate over zones
        if 'V_IDX' not in header:
            for record, loc in zip(records, self.locations):
                for key, value in loc['overrides'].items():
                    if not isinstance(value, (int, float)):
                        continue
                    key = key.upper()
                    if key[:-3] == '_IDX' or key[:2] == 'ID':
                        continue
                    try:
                        record[header_idx[key]] = value
                    except KeyError:
                        continue
            return

        # otherwise, operate over units
        for record, unit in zip(records, self.units):
            overrides = unit['location']['overrides']
            overrides.update(unit['overrides'])
            for key, value in overrides.items():
                if not isinstance(value, (int, float)):
                    continue
                key = key.upper()
                if key[:-3] == '_IDX' or key[:2] == 'ID':
                    continue
                try:
                    idx = header_idx[key]
                except KeyError:
                    continue
                record[idx] = value

    def get(self):
        '''Get data for Muland'''
        data = {}
        headers = self._get_headers()

        # zones
        zone_map, zones_records = self._get_zones()
        data['zones'] = MulandData(header=['I_IDX'] + headers['zones_header'],
                                   records=zones_records)
        self._apply_overrides(data['zones'])

        locations = self.locations
        for location_id, zones_id in zone_map:
            locations[location_id]['zones_id'] = zones_id
        del locations

        # Remove locations not contained by any zones
        outsider_locids = {location['location_id']
                           for location in self.locations
                           if 'zones_id' not in location}
        self.locations = [loc for loc in self.locations
                          if loc['location_id'] not in outsider_locids]
        self.units = [unit for unit in self.units
                      if unit['location']['location_id'] not in outsider_locids]

        # agents
        data['agents'] = MulandData(
            header=['IDAGENT', 'IDMARKET', 'IDAGGRA', 'UPPERBB'] + headers['agents_header'],
            records=self._get_agents_records()
        )
        self._apply_overrides(data['agents'])

        # agents_zones
        data['agents_zones'] = MulandData(
            header=['H_IDX', 'I_IDX', 'ACC', 'P_LN_ATT'] + headers['agents_zones_header'],
            records=self._get_agents_zones_records()
        )
        self._apply_overrides(data['agents_zones'])

        # bids_adjustments
        data['bids_adjustments'] = MulandData(
            header=['H_IDX', 'V_IDX', 'I_IDX', 'BIDADJ'],
            records=self._get_bids_adjustments_records()
        )
        self._apply_overrides(data['bids_adjustments'])

        # bids_functions
        data['bids_functions'] = MulandData(
            header=['IDMARKET', 'IDAGGRA', 'IDATTRIB', 'LINEAPAR', 'CAGENT_X',
                    'CREST_X', 'CACC_X', 'CZONES_X', 'EXPPAR_X', 'CAGENT_Y',
                    'CREST_Y', 'CACC_Y', 'CZONES_Y', 'EXPPAR_Y'],
            records=self._get_bids_functions_records()
        )
        self._apply_overrides(data['bids_functions'])

        # demand
        data['demand'] = MulandData(
            header=['H_IDX', 'DEMAND'],
            records=self._get_demand_records()
        )
        self._apply_overrides(data['demand'])

        # demand_exogenous_cutoff
        data['demand_exogenous_cutoff'] = MulandData(
            header=['H_IDX', 'V_IDX', 'I_IDX', 'DCUTOFF'],
            records=self._get_demand_exogenous_cutoff_records()
        )
        self._apply_overrides(data['demand_exogenous_cutoff'])

        # real_estates_zones
        data['real_estates_zones'] = MulandData(
            header=['V_IDX', 'I_IDX', 'M_IDX'] + headers['real_estates_zones_header'],
            records=self._get_real_estates_zones()
        )
        self._apply_overrides(data['real_estates_zones'])

        # rent_adjustments
        data['rent_adjustments'] = MulandData(
            header=['V_IDX', 'I_IDX', 'RENTADJ'],
            records=self._get_rent_adjustments()
        )
        self._apply_overrides(data['rent_adjustments'])

        # rent_funtions
        data['rent_functions'] = MulandData(
            header=['IDMARKET', 'IDATTRIB', 'SCALEPAR', 'LINEAPAR', 'CREST_X',
                    'CZONES_X', 'EXPPAR_X', 'CREST_Y', 'CZONES_Y', 'EXPPAR_Y'],
            records=self._get_rent_functions()
        )
        self._apply_overrides(data['rent_functions'])

        # subsidies
        data['subsidies'] = MulandData(
            header=['H_IDX', 'V_IDX', 'I_IDX', 'SUBSIDIES'],
            records=self._get_subsidies()
        )
        self._apply_overrides(data['subsidies'])

        # supply
        data['supply'] = MulandData(
            header=['V_IDX', 'I_IDX', 'NREST'],
            records=self._get_supply()
        )
        self._apply_overrides(data['supply'])

        return data

    def _get_headers(self):
        '''Get CSV header records'''
        db_models = db.models

        s = (select([db_models.c.zones_header,
                    db_models.c.agents_header,
                    db_models.c.agents_zones_header,
                    db_models.c.real_estates_zones_header])
            .where(db_models.c.id == self.models_id)
            .limit(1))

        result = self.conn.execute(s)
        header = dict(result.fetchone())
        result.close()


        return header

    # zones
    #"I_IDX";"INDAREA";"COMAREA";"SERVAREA";"TOTAREA";"TOTBUILT";"INCOMEHH";"DIST_ACC"
    #1.00;2.7441056;0.4679935;3.2301371;8968.0590000;10.9089400;0.00;2.8959340
    def _get_zones(self):
        '''Get zones records

        Returns tuple (zone_map, records). The zone_map field carries a
        list of tuples (point_id, zone_id). The records field carries a list
        of records for the zones file.
        '''
        db_zones = db.zones

        values = ', '.join(
            ['(%s, ST_Transform(ST_SetSRID(ST_Point(%s, %s), 4326), 900913))' %
             (loc['location_id'], loc['lng'], loc['lat'])
             for loc in self.locations])

        s = (select([text('locs.id'),
                     db_zones.c.id,
                     db_zones.c.data])
            .select_from(db_zones
                .join(text('(VALUES %s) AS locs (id, geom) ' % values),
                      func.ST_Contains(db_zones.c.area, text('locs.geom'))))
            .where(db_zones.c.models_id == self.models_id)
            .order_by(text('locs.id')))

        result = self.conn.execute(s)
        zone_map = []
        records = []
        for row in result:
            data = [row[0] + 1]
            data.extend(row[2])
            records.append(data)
            zone_map.append([row[0], row[1]])
        result.close()

        return zone_map, records

    # agents
    #"IDAGENT";"IDMARKET";"IDAGGRA";"UPPERBB";"HHINC";"RHO";"FNIP";"ONES"
    #1.00;1.00;1.00;50000.00;674.8841398;11.8789000;0.00;1.00
    def _get_agents_records(self):
        '''Get agents records'''
        db_agents = db.agents

        s = (select([db_agents.c.id,
                     db_agents.c.markets_id,
                     db_agents.c.aggra_id,
                     db_agents.c.upperbb,
                     db_agents.c.data])
            .where(db_agents.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = []
        for row in db.engine.execute(s):
            data = list(row[0:4])
            data.extend(row[4])
            records.append(data)
        result.close()

        return records

    # agents_zones
    #"H_IDX";"I_IDX";"ACC";"P_LN_ATT"
    #1.00;1.00;0.7308194;0.0000000
    def _get_agents_zones_records(self):
        '''Get agents records'''
        db_azones = db.agents_zones

        values = ', '.join(['(%s, %s)' %
                            (location['location_id'] + 1, location['zones_id'])
                            for location in self.locations])

        if not values:
            return []

        s = (select([db_azones.c.agents_id,
                     text('locs.id'),
                     db_azones.c.acc,
                     db_azones.c.att,
                     db_azones.c.data])
            .select_from(db_azones
                .join(text('(VALUES %s) AS locs (id, zones_id) ' % values),
                      db_azones.c.zones_id == text('locs.zones_id')))
            .where(db_azones.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = []
        for row in db.engine.execute(s):
            data = list(row[0:4])
            data.extend(row[4])
            records.append(data)
        result.close()

        return records

    # bids_adjustments
    #"H_IDX";"V_IDX";"I_IDX";"BIDADJ"
    #1.00;1.00;1.00;0.0000000000
    def _get_bids_adjustments_records(self):
        '''Get bids_adjustments records'''
        db_badj = db.bids_adjustments

        values = ', '.join(['(%s, %s, %s)' %
                            (unit['location']['location_id'] + 1,
                             unit['location']['zones_id'],
                             unit['types_id'])
                            for unit in self.units])

        if not values:
            return []

        s = (select([db_badj.c.agents_id,
                     db_badj.c.types_id,
                     text('units.lid'),
                     db_badj.c.bidadj])
            .select_from(db_badj
                .join(text('(VALUES %s) AS units (lid, zones_id, types_id) ' % values),
                      and_(db_badj.c.zones_id == text('units.zones_id'),
                           db_badj.c.types_id == text('units.types_id'))))
            .where(db_badj.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = [list(row) for row in result]
        result.close()

        return records

    # bids_functions
    #"IDMARKET";"IDAGGRA";"IDATTRIB";"LINEAPAR";"CAGENT_X";"CREST_X";"CACC_X";"CZONES_X";"EXPPAR_X";"CAGENT_Y";"CREST_Y";"CACC_Y";"CZONES_Y";"EXPPAR_Y"
    #1.0000;1.0000;1.0000;15.7300;0.0000;5.0000;0.0000;0.0000;1.0000;0.0000;0.0000;0.0000;0.0000;0.0000
    def _get_bids_functions_records(self):
        '''Get bids_functions records'''
        db_bfunc = db.bids_functions

        s = (select([db_bfunc.c.markets_id,
                     db_bfunc.c.aggra_id,
                     db_bfunc.c.idattrib,
                     db_bfunc.c.lineapar,
                     db_bfunc.c.cagent_x,
                     db_bfunc.c.crest_x,
                     db_bfunc.c.cacc_x,
                     db_bfunc.c.czones_x,
                     db_bfunc.c.exppar_x,
                     db_bfunc.c.cagent_y,
                     db_bfunc.c.crest_y,
                     db_bfunc.c.cacc_y,
                     db_bfunc.c.czones_y,
                     db_bfunc.c.exppar_y])
            .where(db_bfunc.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = [list(row) for row in result]
        result.close()

        return records

    # demand
    #"H_IDX";"DEMAND"
    #1.00;10562.7974402
    def _get_demand_records(self):
        '''Get demand records'''
        db_demand = db.demand

        s = (select([db_demand.c.agents_id,
                     db_demand.c.demand])
            .where(db_demand.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = [list(row) for row in result]
        result.close()

        return records

    # demand_exogenous_cutoff
    #"H_IDX";"V_IDX";"I_IDX";"DCUTOFF"
    #1.00;1.00;1.00;1.00
    def _get_demand_exogenous_cutoff_records(self):
        '''Get demand_exogenous_cutoff records'''
        db_decutoff = db.demand_exogenous_cutoff

        values = ', '.join(['(%s, %s, %s)' %
                            (unit['location']['location_id'] + 1,
                             unit['location']['zones_id'],
                             unit['types_id'])
                            for unit in self.units])

        if not values:
            return []

        s = (select([db_decutoff.c.agents_id,
                     db_decutoff.c.types_id,
                     text('units.lid'),
                     db_decutoff.c.dcutoff])
            .select_from(db_decutoff
                .join(text('(VALUES %s) AS units (lid, zones_id, types_id) ' % values),
                      and_(db_decutoff.c.zones_id == text('units.zones_id'),
                           db_decutoff.c.types_id == text('units.types_id'))))
            .where(db_decutoff.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = [list(row) for row in result]
        result.close()

        return records

    # real_estates_zones
    #"V_IDX";"I_IDX";"M_IDX";"LOTSIZE";"BUILT";"IS_HOUSE";"IS_APT"
    #1.00;1.00;1.00;3.4800000;0.027670;1.00;0.00
    def _get_real_estates_zones(self):
        '''Get real_estates_zones records'''
        db_rezones = db.real_estates_zones

        values = ', '.join(['(%s, %s, %s)' %
                            (unit['location']['location_id'] + 1,
                             unit['location']['zones_id'],
                             unit['types_id'])
                            for unit in self.units])

        if not values:
            return []

        s = (select([db_rezones.c.types_id,
                     text('units.lid'),
                     db_rezones.c.markets_id,
                     db_rezones.c.data])
            .select_from(db_rezones
                .join(text('(VALUES %s) AS units (lid, zones_id, types_id) ' % values),
                      and_(db_rezones.c.zones_id == text('units.zones_id'),
                           db_rezones.c.types_id == text('units.types_id'))))
            .where(db_rezones.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = []
        for row in result:
            data = list(row[:3])
            data.extend(row[3])
            records.append(data)

        result.close()
        return records

    # rent_adjustments
    #"V_IDX";"I_IDX";"RENTADJ"
    #1.00;1.00;0.00
    def _get_rent_adjustments(self):
        '''Get rent_adjustments records'''
        db_rentadj = db.rent_adjustments

        values = ', '.join(['(%s, %s, %s)' %
                            (unit['location']['location_id'] + 1,
                             unit['location']['zones_id'],
                             unit['types_id'])
                            for unit in self.units])

        if not values:
            return []

        s = (select([db_rentadj.c.types_id,
                     text('units.lid'),
                     db_rentadj.c.adjustment])
            .select_from(db_rentadj
                .join(text('(VALUES %s) AS units (lid, zones_id, types_id) ' % values),
                      and_(db_rentadj.c.zones_id == text('units.zones_id'),
                           db_rentadj.c.types_id == text('units.types_id'))))
            .where(db_rentadj.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = [list(row) for row in result]
        result.close()

        return records

    # rent_functions
    #"IDMARKET";"IDATTRIB";"SCALEPAR";"LINEAPAR";"CREST_X";"CZONES_X";"EXPPAR_X";"CREST_Y";"CZONES_Y";"EXPPAR_Y"
    #1.00;1.00;0.4000000000;0.323614000;5.00;0.00;1.00;0.00;0.00;0.00
    def _get_rent_functions(self):
        '''Get rent_functions records'''
        db_rentfunc = db.rent_functions

        s = (select([db_rentfunc.c.markets_id,
                     db_rentfunc.c.idattrib,
                     db_rentfunc.c.scalepar,
                     db_rentfunc.c.lineapar,
                     db_rentfunc.c.crest_x,
                     db_rentfunc.c.czones_x,
                     db_rentfunc.c.exppar_x,
                     db_rentfunc.c.crest_y,
                     db_rentfunc.c.czones_y,
                     db_rentfunc.c.exppar_y])
            .where(db_rentfunc.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = [list(row) for row in result]
        result.close()

        return records

    # subsidies
    #"H_IDX";"V_IDX";"I_IDX";"SUBSIDIES"
    #1.00;1.00;1.00;0.0000000000
    def _get_subsidies(self):
        '''Get subsidies records'''
        db_subsidies = db.subsidies

        values = ', '.join(['(%s, %s, %s)' %
                            (unit['location']['location_id'] + 1,
                             unit['location']['zones_id'],
                             unit['types_id'])
                            for unit in self.units])

        if not values:
            return []

        s = (select([db_subsidies.c.agents_id,
                     db_subsidies.c.types_id,
                     text('unit.lid'),
                     db_subsidies.c.subsidies])
            .select_from(db_subsidies
                .join(text('(VALUES %s) AS unit (lid, zones_id, types_id) ' % values),
                      and_(db_subsidies.c.zones_id == text('unit.zones_id'),
                           db_subsidies.c.types_id == text('unit.types_id'))))
            .where(db_subsidies.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = [list(row) for row in result]
        result.close()

        return records

    # supply
    #"V_IDX";"I_IDX";"NREST"
    #1.00;1.00;0.0000000000
    def _get_supply(self):
        '''Get supply records'''
        db_supply = db.supply

        values = ', '.join(['(%s, %s, %s)' %
                            (unit['location']['location_id'] + 1,
                             unit['location']['zones_id'],
                             unit['types_id'])
                            for unit in self.units])

        if not values:
            return []

        s = (select([db_supply.c.types_id,
                     text('unit.lid'),
                     db_supply.c.nrest])
            .select_from(db_supply
                .join(text('(VALUES %s) AS unit (lid, zones_id, types_id) ' % values),
                      and_(db_supply.c.zones_id == text('unit.zones_id'),
                           db_supply.c.types_id == text('unit.types_id'))))
            .where(db_supply.c.models_id == self.models_id))

        result = self.conn.execute(s)
        records = [list(row) for row in result]
        result.close()

        return records

class ModelImporter:
    '''Import models into the database'''
    # pylint: disable=too-few-public-methods,too-many-instance-attributes,no-value-for-parameter
    _insert_limit = 3000 # how many rows will be inserted at once

    def __init__(self, name, srid=4326, verbose=False):
        self.name = name
        self.zones_csv = '%s/zones.csv' % name
        self.agents_csv = '%s/agents.csv' % name
        self.agents_zones_csv = '%s/agents_zones.csv' % name
        self.real_estates_zones_csv = '%s/real_estates_zones.csv' % name
        self.rent_adjustments_csv = '%s/rent_adjustments.csv' % name
        self.supply_csv = '%s/supply.csv' % name
        self.demand_csv = '%s/demand.csv' % name
        self.subsidies_csv = '%s/subsidies.csv' % name
        self.demand_exogenous_cutoff_csv = '%s/demand_exogenous_cutoff.csv' % name
        self.bids_adjustments_csv = '%s/bids_adjustments.csv' % name
        self.bids_functions_csv = '%s/bids_functions.csv' % name
        self.rent_functions_csv = '%s/rent_functions.csv' % name
        self.shapefile = '%s/%s.shp' % (name, name)
        self.models_id = None
        self.srid = srid
        self.verbose = verbose

    def import_model(self):
        '''Run all the steps to import a model'''
        self.models_id = self.db_create_model()
        self.db_import_zones()
        self.db_import_rent_adjustments()
        self.db_import_supply()
        self.db_import_real_estates_zones()
        self.db_import_agents()
        self.db_import_demand()
        self.db_import_subsidies()
        self.db_import_demand_exogenous_cutoff()
        self.db_import_agents_zones()
        self.db_import_bids_adjustments()
        self.db_import_bids_functions()
        self.db_import_rent_functions()

    def db_create_model(self):
        '''Create entry for the model at the db and returns its id'''
        # Find headers
        with open(self.zones_csv) as f:
            reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            zones_header = tuple(next(reader)[1:])

        with open(self.agents_csv) as f:
            reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            agents_header = tuple(next(reader)[4:])

        with open(self.agents_zones_csv) as f:
            reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            agents_zones_header = tuple(next(reader)[4:])

        with open(self.real_estates_zones_csv) as f:
            reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            real_estates_zones_header = tuple(next(reader)[3:])

        # Insert model
        s = db.models.insert().values(
            name=self.name,
            zones_header=zones_header,
            agents_header=agents_header,
            agents_zones_header=agents_zones_header,
            real_estates_zones_header=real_estates_zones_header
        ).returning(db.models.c.id)

        result = db.engine.execute(s)
        models_id = result.fetchone()[0]
        result.close()

        return models_id

    def _get_zone_shapes(self):
        '''Parse shapefile and return mapping between zone_id and polygon wkt'''
        sf = shapefile.Reader(self.shapefile)
        fields = [x[0] for x in sf.fields[1:]]

        zone_wkt = {}
        for sr in sf.shapeRecords():
            assert sr.shape.shapeType == 5 # Polygon

            # find zones_id
            srfields = dict(zip(fields, sr.record))
            zones_id = srfields['ID']

            # find polygon rings
            parts = sr.shape.parts
            points = sr.shape.points
            ringidx = list(zip_longest(parts, parts[1:]))
            exterior = points[ringidx[0][0]:ringidx[0][1]]
            interior = [points[i:j] for i, j in ringidx[1:]]

            # generate polygon wkt
            polygon = Polygon(exterior, interior)
            wkt = polygon.wkt
            zone_wkt[zones_id] = wkt

        return zone_wkt

    def _insert_with_limit(self, table, values):
        '''Insert values into table respecting limit per query'''
        verbose = self.verbose
        insert_limit = self._insert_limit
        conn = db.engine.connect()
        while True:
            viter = iter(values)
            partial_values = []
            for _ in range(insert_limit):
                try:
                    partial_values.append(next(viter))
                except StopIteration:
                    break
            if len(partial_values) == 0:
                return
            result = conn.execute(table.insert().values(partial_values))
            result.close()
            if verbose is True and len(partial_values) > 0:
                print('Inserted %d rows into %s' % (len(partial_values),
                                                    str(table)))
            if len(partial_values) < insert_limit:
                return

    def db_import_zones(self):
        '''Import zones.csv'''
        assert self.models_id is not None

        zone_wkt = self._get_zone_shapes()

        # Parse zone file
        with open(self.zones_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r) # skip header
            models_id = self.models_id
            srid = self.srid
            values = ({
                'models_id': models_id,
                'id': int(row[0]),
                'data': tuple(row[1:]),
                'area': func.ST_Transform(
                            func.ST_GeomFromText(zone_wkt[int(row[0])],
                                                 srid),
                            900913)
            } for row in r)
            self._insert_with_limit(db.zones, values)

    def db_import_rent_adjustments(self):
        '''Import rent_adjustments.csv'''
        assert self.models_id is not None

        values = []
        with open(self.rent_adjustments_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r)
            values = ({'types_id': int(row[0]), 'zones_id': int(row[1]),
                       'models_id': self.models_id, 'adjustment': row[2]}
                       for row in r)
            self._insert_with_limit(db.rent_adjustments, values)

    def db_import_supply(self):
        '''Import supply.csv'''
        assert self.models_id is not None

        with open(self.supply_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r)
            values = ({'types_id': int(row[0]),
                       'zones_id': int(row[1]),
                       'models_id': self.models_id,
                       'nrest': row[2]}
                      for row in r)
            self._insert_with_limit(db.supply, values)

    def db_import_real_estates_zones(self):
        '''Import real_estates_zones.csv'''
        assert self.models_id is not None

        with open(self.real_estates_zones_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r)
            values = ({'models_id': self.models_id,
                       'types_id': int(row[0]),
                       'zones_id': int(row[1]),
                       'markets_id': int(row[2]),
                       'data': tuple(row[3:])}
                      for row in r)
            self._insert_with_limit(db.real_estates_zones, values)

    def db_import_agents(self):
        '''Import agents.csv'''
        assert self.models_id is not None

        with open(self.agents_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r) # skip header
            values = ({'models_id': self.models_id,
                       'id': row[0],
                       'markets_id': row[1],
                       'aggra_id': row[2],
                       'upperbb': row[3],
                       'data': tuple(row[4:])}
                      for row in r)
            self._insert_with_limit(db.agents, values)

    def db_import_demand(self):
        '''Import demand.csv'''
        assert self.models_id is not None

        with open(self.demand_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r) # skip header
            values = ({'models_id': self.models_id,
                       'agents_id': row[0],
                       'demand': row[1]}
                      for row in r)
            self._insert_with_limit(db.demand, values)

    def db_import_subsidies(self):
        '''Import subsidies.csv'''
        assert self.models_id is not None

        with open(self.subsidies_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r) # skip header
            values = ({'models_id': self.models_id, 'agents_id': row[0],
                       'types_id': row[1], 'zones_id': row[2],
                       'subsidies': row[3]}
                       for row in r)
            self._insert_with_limit(db.subsidies, values)

    def db_import_demand_exogenous_cutoff(self):
        '''Import demand_exogenous_cutoff.csv'''
        assert self.models_id is not None

        with open(self.demand_exogenous_cutoff_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r) # skip header
            values = ({'models_id': self.models_id, 'agents_id': row[0],
                       'types_id': row[1], 'zones_id': row[2],
                       'dcutoff': row[3]}
                       for row in r)
            self._insert_with_limit(db.demand_exogenous_cutoff, values)

    def db_import_agents_zones(self):
        '''Import agents_zones.csv'''
        assert self.models_id is not None

        with open(self.agents_zones_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r) # skip header
            values = ({'models_id': self.models_id, 'agents_id': row[0],
                       'zones_id': row[1], 'acc': row[2], 'att': row[3],
                       'data': tuple(row[4:])}
                      for row in r)
            self._insert_with_limit(db.agents_zones, values)

    def db_import_bids_adjustments(self):
        '''Import bids_adjustments.csv'''
        assert self.models_id is not None

        with open(self.bids_adjustments_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r) # skip header
            values = ({'models_id': self.models_id, 'agents_id': row[0],
                       'types_id': row[1], 'zones_id': row[2],
                       'bidadj': row[3]}
                      for row in r)
            self._insert_with_limit(db.bids_adjustments, values)

    def db_import_bids_functions(self):
        '''Import bids_functions.csv'''
        assert self.models_id is not None

        with open(self.bids_functions_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r) # skip header
            values = ({'models_id': self.models_id, 'markets_id': row[0],
                       'aggra_id': row[1], 'idattrib': row[2],
                       'lineapar': row[3], 'cagent_x': row[4],
                       'crest_x': row[5], 'cacc_x': row[6],
                       'czones_x': row[7], 'exppar_x': row[8],
                       'cagent_y': row[9], 'crest_y': row[10],
                       'cacc_y': row[11], 'czones_y': row[12],
                       'exppar_y': row[13]}
                      for row in r)
            self._insert_with_limit(db.bids_functions, values)


    def db_import_rent_functions(self):
        '''Import rent_functions.csv'''
        assert self.models_id is not None

        with open(self.rent_functions_csv) as f:
            r = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            next(r) # skip header
            values = ({'models_id': self.models_id, 'markets_id': row[0],
                       'idattrib': row[1], 'scalepar': row[2],
                       'lineapar': row[3], 'crest_x': row[4],
                       'czones_x': row[5], 'exppar_x': row[6],
                       'crest_y': row[7], 'czones_y': row[8],
                       'exppar_y': row[9]}
                      for row in r)
            self._insert_with_limit(db.rent_functions, values)
