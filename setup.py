from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-feedNTI',
    version=version,
    description="Feed con la estructura de NTI y datos.gob.es para poder federar con ellos.",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='ggjuanes',
    author_email='ggjuanes@gmail.com',
    url='http://github.com/opendatacanarias/ckanext-feedNTI',
    license='mit',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.feedNTI'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        # myplugin=ckanext.feedNTI.plugin:PluginClass
	feedNTI=ckanext.feedNTI.plugin:RoutingFeedAtomNTI
    ''',
)
