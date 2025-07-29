# -*- coding: utf-8 -*-
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config

log = logging.getLogger(__name__)


class DatapusherPlusApiPlugin(plugins.SingletonPlugin):
    """Plugin pour exposer une API REST pour datapusher plus"""
    
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer
    def update_config(self, config_):
        """Mise à jour de la configuration CKAN"""
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'datapusherplusapi')

    # IBlueprint
    def get_blueprint(self):
        """Retourne le blueprint pour les routes API"""
        from ckanext.datapusherplusapi.views import get_blueprints
        return get_blueprints()
