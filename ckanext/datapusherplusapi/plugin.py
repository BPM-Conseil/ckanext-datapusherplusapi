# -*- coding: utf-8 -*-
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

log = logging.getLogger(__name__)


class DatapusherPlusApiPlugin(plugins.SingletonPlugin):
    """Plugin to expose a REST API for datapusher plus"""
    
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer
    def update_config(self, config_):
        """Update CKAN configuration"""
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'datapusherplusapi')

    # IBlueprint
    def get_blueprint(self):
        """Return the blueprint for API routes"""
        from ckanext.datapusherplusapi.views import get_blueprints
        return get_blueprints()
