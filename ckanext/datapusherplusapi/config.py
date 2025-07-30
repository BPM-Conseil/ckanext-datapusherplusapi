# -*- coding: utf-8 -*-
"""
Configuration par défaut pour le plugin datapusher plus API
"""

# Configuration par défaut
DEFAULT_CONFIG = {    
    # Timeout pour les requêtes (en secondes)
    'ckanext.datapusher_plus.timeout': 30
}


def get_config_value(key, default=None):
    """
    Récupère une valeur de configuration
    
    Args:
        key (str): Clé de configuration
        default: Valeur par défaut si la clé n'existe pas
        
    Returns:
        Valeur de configuration
    """
    from ckan.common import config
    return config.get(key, default or DEFAULT_CONFIG.get(key))
