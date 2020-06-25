# coding: utf-8

from . import config
import bottle
bottle.BaseRequest.MEMFILE_MAX = config.mulandweb_memfile_max

app = bottle.Bottle()

from . import handlers
