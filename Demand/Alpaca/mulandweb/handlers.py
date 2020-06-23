#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=invalid-name,
'''Provides request handlers for MulandWeb'''

import re
import json
import codecs
import bottle

from .muland import Muland, MulandRunError
from .mulanddb import MulandDB, ModelNotFound
from . import xmlparser
from . import app

__all__ = ['post_handler']

_model_re = re.compile('[a-z]')
_utf8reader = codecs.getreader('utf-8')

@app.post('/<model>')
def post_handler(model): # pylint: disable=too-many-branches,too-many-statements
    '''Handles POST requests to server'''
    # Validate model name
    if _model_re.match(model) is None:
        raise bottle.HTTPError(404)

    # Extract data acoording to Content-Type
    ctype = bottle.request.headers['Content-Type'].lower() # pylint: disable=unsubscriptable-object
    mime = ctype.split(';')[0]
    if mime == 'application/json':
        data_in = bottle.request.json
        output_mime = 'json'
    elif mime == 'application/xml' or mime == 'text/xml':
        if 'charset=utf-8' not in ctype:
            raise bottle.HTTPError(400, 'Specify charset=utf-8 for '
                                        'for this MIME type.')
        loc = xmlparser.load(_utf8reader(bottle.request.body))
        data_in = {'loc': loc} # pylint: disable=redefined-variable-type
        output_mime = 'xml'
    else:
        raise bottle.HTTPError(400, 'Invalid Content-Type')

    # Prepare data
    if data_in is None:
        raise bottle.HTTPError(400, 'No input data.')

    if not isinstance(data_in, dict):
        raise bottle.HTTPError(400, 'Input data isn\'t an object.')

    if 'loc' not in data_in:
        raise bottle.HTTPError(400, "'loc' is not present at input data.")

    locations = data_in['loc']
    if not isinstance(locations, list):
        raise bottle.HTTPError(400, "'loc' isn't an array")

    for loc in locations:
        if 'lnglat' not in loc:
            raise bottle.HTTPError(400, "'lnglat' not in 'loc' items")

        lnglat = loc['lnglat']
        if not isinstance(lnglat, list) or len(lnglat) != 2:
            raise bottle.HTTPError(400, "'lnglat' isn't array with 2 elements")

        if not all((isinstance(x, (int, float)) for x in lnglat)):
            raise bottle.HTTPError(400, "lng or lat not a number")

        if 'units' not in loc:
            raise bottle.HTTPError(400, "'units' not in 'loc' items")
        units = loc['units']
        if not isinstance(units, list):
            raise bottle.HTTPError(400, "'units' isn't an array")

        for unit in units:
            if 'type' not in unit:
                raise bottle.HTTPError(400, "'type' not in unit")
            if not isinstance(unit['type'], (int, float)):
                raise bottle.HTTPError(400, "'type' isn't a number")

    # Get data from MulandDB
    try:
        mudata = MulandDB(model, locations).get()
    except ModelNotFound:
        raise bottle.HTTPError(404)

    # Run Mu-Land
    mu = Muland(**mudata)
    try:
        mu.run()
    except MulandRunError as e:
        raise bottle.HTTPError(500, exception=e)

    # Send response
    if output_mime == 'json':
        bottle.response.headers['Content-Type'] = 'application/json'
        return json.dumps(mu.output_data)
    elif output_mime == 'xml':
        bottle.response.headers['Content-Type'] = 'application/xml; charset=utf-8'
        return xmlparser.dumps(mu.output_data)
