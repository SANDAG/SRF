# coding: utf-8

import argparse
from . import config

def run(host=config.mulandweb_host, port=config.mulandweb_port):
    '''Run server on Gunicorn'''
    from . import app
    from gunicorn.app.base import Application
    gunicorn_config = {'bind': "%s:%d" % (host, port)}
    class GunicornApplication(Application):
        def __init__(self):
            self.application = app
            self.options = {'bind': "%s:%d" % (host, port)}
            super().__init__()
        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key.lower(), value)
        def load(self):
            return self.application
    GunicornApplication().run()

def import_model(name, srid=4326):
    '''Import model into database'''
    from .mulanddb import ModelImporter
    ModelImporter(name=name, srid=srid, verbose=True).import_model()

def create_tables():
    '''Create MulandWeb tables'''
    from . import db
    db.create_tables()

def main():
    '''Main function'''
    parser = argparse.ArgumentParser(prog='mulandweb', description='MulandWeb')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('-r', '--run', action='store_true',
                        help='run mulandweb on gunicorn')
    action.add_argument('-i', '--import', dest='import_name',
                        metavar='model_name', type=str, nargs='?', default=None,
                        help="import model 'model_name' with name 'model_name'")
    action.add_argument('-c', '--create-tables', action='store_true',
                        help='create mulandweb tables at the database.')
    parser.add_argument('--import-srid', dest='srid',
                        metavar='srid', type=int, nargs='?', default=4326,
                        help='specify SRID used in shape files when importing')
    args = parser.parse_args()

    if args.run:
        run()
        return

    if args.import_name:
        import_model(args.import_name, srid=args.srid)
        return

    if args.create_tables:
        create_tables()
        return

main()
