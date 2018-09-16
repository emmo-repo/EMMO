#!/usr/bin/env python
"""Python reference API for the Europeean Materials
Modelling Ontology (EMMO).
"""

from distutils.core import setup


setup(name='emmo',
      version='0.1',
      description = 'Python reference API for the Europeean Materials Modelling Ontology',
      long_description=__doc__,
      author='Europeean Materials Modelling Council (EMMC)',
      author_email='jesper.friis@sintef.no',
      url='https://github.com/nanodome/emmo',
      packages=['emmo'],
      scripts=[],
      #license='',
      python_requires='>=3.4.0',
      package_dir={'emmo': 'emmo'},
      package_data={'emmo': ['tests/*.py']},
      data_files=[
          ('owl', ['../emmo/owl/emmo.owl']),
          ('.', ['../README.md']),
          ]
     )
