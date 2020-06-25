# coding: utf-8

from setuptools import setup

setup(name='mulandweb',
      version='0.6',
      description='Web Interface for the Muland Application',
      url='https://bitbucket.org/leandropls/mulandweb',
      author='Leandro Pereira de Lima e Silva',
      author_email='leandro@limaesilva.com.br',
      license='MIT',
      packages=['mulandweb'],
      install_requires=[
        'bottle',
        'gunicorn',
        'GeoAlchemy2',
        'psycopg2',
        'SQLAlchemy',
        'pyshp',
        'shapely',
        'defusedxml',
      ],
      zip_safe=False)
