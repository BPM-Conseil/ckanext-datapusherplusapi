from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name='ckanext-datapusherplusapi',
    version=version,
    description="CKAN extension providing REST API for datapusher plus file submission",
    long_description='''
    This extension provides a REST API endpoint to submit files to datapusher plus.
    Compatible with CKAN 2.9.x.
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='CKAN datapusher API REST',
    author='Data4Citizen',
    author_email='',
    url='',
    license='AGPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ckan>=2.9.0',
        'requests',
    ],
    entry_points='''
        [ckan.plugins]
        datapusherplusapi=ckanext.datapusherplusapi.plugin:DatapusherPlusApiPlugin
        
        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
    ''',
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    }
)
