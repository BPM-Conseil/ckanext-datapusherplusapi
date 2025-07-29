# -*- coding: utf-8 -*-
"""
Fonctions utilitaires pour le plugin datapusher plus API
"""
import logging
import requests
from urllib.parse import urlparse
import ckan.plugins.toolkit as toolkit
from ckanext.datapusherplusapi.config import get_config_value, is_format_supported

log = logging.getLogger(__name__)


def get_resource_file_info(resource):
    """
    Récupère les informations d'un fichier de ressource
    
    Args:
        resource (dict): Dictionnaire de la ressource CKAN
        
    Returns:
        dict: Informations sur le fichier (format, taille, etc.)
    """
    file_info = {
        'format': resource.get('format', '').lower(),
        'url': resource.get('url', ''),
        'size': resource.get('size'),
        'name': resource.get('name', ''),
        'id': resource.get('id')
    }
    
    # Détection du format depuis l'URL si pas spécifié
    if not file_info['format'] and file_info['url']:
        parsed_url = urlparse(file_info['url'])
        if parsed_url.path:
            file_extension = parsed_url.path.split('.')[-1].lower()
            if file_extension in ['csv', 'tsv', 'xls', 'xlsx', 'ods', 'json', 'xml']:
                file_info['format'] = file_extension
    
    return file_info


def validate_resource_for_datapusher(resource):
    """
    Valide qu'une ressource peut être traitée par datapusher plus
    
    Args:
        resource (dict): Dictionnaire de la ressource CKAN
        
    Returns:
        tuple: (is_valid, error_message)
    """
    file_info = get_resource_file_info(resource)
    
    # Vérification du format
    if not file_info['format']:
        return False, "Format de fichier non détecté"
    
    if not is_format_supported(file_info['format']):
        supported = get_config_value('ckanext.datapusher_plus.supported_formats')
        return False, f"Format '{file_info['format']}' non supporté. Formats supportés: {', '.join(supported)}"
    
    # Vérification de l'URL
    if not file_info['url']:
        return False, "URL de la ressource manquante"
    
    # Vérification de la taille si disponible
    if file_info['size']:
        try:
            size_mb = int(file_info['size']) / (1024 * 1024)
            max_size = get_config_value('ckanext.datapusher_plus.max_file_size')
            if size_mb > max_size:
                return False, f"Fichier trop volumineux ({size_mb:.1f}MB). Taille maximum: {max_size}MB"
        except (ValueError, TypeError):
            log.warning(f"Impossible de parser la taille du fichier: {file_info['size']}")
    
    return True, None


def check_datapusher_plus_availability():
    """
    Vérifie que le service datapusher plus est disponible
    
    Returns:
        tuple: (is_available, error_message)
    """
    try:
        datapusher_url = get_config_value('ckanext.datapusher_plus.url')
        timeout = get_config_value('ckanext.datapusher_plus.timeout')
        
        # Test de connexion
        health_url = f"{datapusher_url.rstrip('/')}/health"
        response = requests.get(health_url, timeout=timeout)
        
        if response.status_code == 200:
            return True, None
        else:
            return False, f"Service datapusher plus non disponible (HTTP {response.status_code})"
            
    except requests.exceptions.ConnectionError:
        return False, "Impossible de se connecter au service datapusher plus"
    except requests.exceptions.Timeout:
        return False, "Timeout lors de la connexion au service datapusher plus"
    except Exception as e:
        return False, f"Erreur lors de la vérification: {str(e)}"


def format_job_response(job_data):
    """
    Formate la réponse d'un job datapusher plus
    
    Args:
        job_data (dict): Données du job
        
    Returns:
        dict: Réponse formatée
    """
    return {
        'job_id': job_data.get('job_id'),
        'status': job_data.get('status', 'unknown'),
        'created': job_data.get('created'),
        'finished': job_data.get('finished'),
        'error': job_data.get('error'),
        'logs': job_data.get('logs', []),
        'result': job_data.get('result')
    }


def get_api_key_from_context(context):
    """
    Récupère la clé API depuis le contexte CKAN
    
    Args:
        context (dict): Contexte CKAN
        
    Returns:
        str: Clé API ou None
    """
    # Essayer de récupérer depuis le contexte
    api_key = context.get('apikey')
    if api_key:
        return api_key
    
    # Essayer de récupérer depuis la configuration
    from ckan.common import config
    api_key = config.get('ckan.site_api_key')
    if api_key:
        return api_key
    
    # Essayer de récupérer depuis l'utilisateur actuel
    try:
        user = context.get('user')
        if user:
            user_obj = toolkit.get_action('user_show')(
                {'ignore_auth': True}, {'id': user}
            )
            return user_obj.get('apikey')
    except Exception:
        pass
    
    return None
