# coding: utf-8

'''Configuration parameters of MulandWeb'''

import os

# Muland Binary interface
muland_binary = os.getenv('MULAND_BINARY_PATH', 'bin/muland')
muland_work = os.getenv('MULAND_WORK_PATH', 'work')

# MulandWeb
mulandweb_host = os.getenv('MULANDWEB_HOST', '0.0.0.0')
mulandweb_port = int(os.getenv('MULANDWEB_PORT', 8000))
mulandweb_memfile_max = int(os.getenv('MULANDWEB_MEMFILE_MAX', 5 * 1024 * 1024))

# Database
db_url = os.getenv('MULAND_DB_URL', 'postgresql://gis:gis@localhost/gis')
db_prefix = os.getenv('MULAND_DB_PREFIX', '')

try:
    from mulandlocal import *
except ImportError:
    pass
