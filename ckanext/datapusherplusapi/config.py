# -*- coding: utf-8 -*-
"""
Configuration par défaut pour le plugin datapusher plus API
"""

# Configuration par défaut
DEFAULT_CONFIG = {
    # URL du service datapusher plus
    'ckanext.datapusher_plus.url': 'http://datapusher-plus:8800',
    
    # Timeout pour les requêtes (en secondes)
    'ckanext.datapusher_plus.timeout': 30,
    
    # Nombre maximum de tentatives
    'ckanext.datapusher_plus.max_retries': 3,
    
    # Types de fichiers supportés
    'ckanext.datapusher_plus.supported_formats': [
        'csv', 'tsv', 'xls', 'xlsx', 'ods', 'json', 'xml'
    ],
    
    # Taille maximum des fichiers (en MB)
    'ckanext.datapusher_plus.max_file_size': 100,
    
    # Activer les logs détaillés
    'ckanext.datapusher_plus.debug': False
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


def is_format_supported(file_format):
    """
    Vérifie si un format de fichier est supporté
    
    Args:
        file_format (str): Format du fichier
        
    Returns:
        bool: True si supporté, False sinon
    """
    supported_formats = get_config_value('ckanext.datapusher_plus.supported_formats')
    return file_format.lower() in [fmt.lower() for fmt in supported_formats]


def validate_file_size(file_size_mb):
    """
    Valide la taille d'un fichier
    
    Args:
        file_size_mb (float): Taille du fichier en MB
        
    Returns:
        bool: True si la taille est acceptable, False sinon
    """
    max_size = get_config_value('ckanext.datapusher_plus.max_file_size')
    return file_size_mb <= max_size
