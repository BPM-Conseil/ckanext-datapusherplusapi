# -*- coding: utf-8 -*-
"""
Default configuration for the datapusher plus API plugin
"""

# Default configuration
DEFAULT_CONFIG = {    
    # Request timeout (in seconds)
    'ckanext.datapusher_plus.timeout': 30
}


def get_config_value(key, default=None):
    """
    Get a configuration value
    
    Args:
        key (str): Configuration key
        default: Default value if key doesn't exist
        
    Returns:
        Configuration value
    """
    from ckan.common import config
    return config.get(key, default or DEFAULT_CONFIG.get(key))
