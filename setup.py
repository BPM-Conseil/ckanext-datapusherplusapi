from setuptools import setup, find_packages

setup(
    name='ckanext-datapusherplusapi',
    version='0.0.1',
    description='Trigger DataPusher+ via API',
    author='BPM Conseil',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points='''
        [ckan.plugins]
        datapusherplusapi=ckanext.datapusherplusapi.plugin:DatapusherAPIPlugin
    ''',
)
