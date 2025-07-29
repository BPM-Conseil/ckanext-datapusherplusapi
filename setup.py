from setuptools import setup

setup(
    name='ckanext-datapusherplusapi',
    version='0.0.1',
    description='Trigger DataPusher plus from a custom API endpoint',
    author='BPM-Conseil',
    packages=['ckanext.datapusherplusapi'],
    install_requires=[],
    entry_points='''
        [ckan.plugins]
        datapusherplusapi=ckanext.datapusherplusapi.plugin:DatapusherPlusAPIPlugin
    '''
)
