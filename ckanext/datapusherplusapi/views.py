# -*- coding: utf-8 -*-
import json
import logging
import requests
from flask import Blueprint, request, jsonify
import ckan.plugins.toolkit as toolkit
from ckan.common import config
import ckan.model as model
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

datapusherplusapi = Blueprint(
    'datapusherplusapi', 
    __name__,
    url_prefix='/api/3/action'
)


def get_blueprints():
    """Retourne la liste des blueprints"""
    return [datapusherplusapi]


@datapusherplusapi.route('/datapusher_plus_submit', methods=['POST'])
def datapusher_plus_submit():
    """
    API REST pour soumettre un fichier au datapusher plus
    
    Paramètres attendus:
    - resource_id: ID de la ressource CKAN
    - package_id: ID du package CKAN (optionnel)
    - force: Forcer la soumission même si déjà en cours (optionnel, défaut: False)
    
    Retourne:
    - success: True/False
    - message: Message de statut
    - job_id: ID du job datapusher plus (si succès)
    """
    try:
        # Vérification de l'authentification
        context = {'user': toolkit.c.user}
        toolkit.check_access('resource_update', context)
        
        # Récupération des paramètres
        data = request.get_json() or {}
        resource_id = data.get('resource_id')
        package_id = data.get('package_id')
        force = data.get('force', False)
        
        if not resource_id:
            return jsonify({
                'success': False,
                'error': 'resource_id est requis'
            }), 400
        
        # Vérification que la ressource existe
        try:
            resource = toolkit.get_action('resource_show')(
                context, {'id': resource_id}
            )
        except toolkit.ObjectNotFound:
            return jsonify({
                'success': False,
                'error': f'Ressource {resource_id} non trouvée'
            }), 404
        
        # Récupération de l'URL du datapusher plus depuis la config
        datapusher_plus_url = config.get('ckanext.datapusher_plus.url', 
                                       'http://datapusher-plus:8800')
        
        # Préparation des données pour datapusher plus
        job_data = {
            'resource_id': resource_id,
            'resource_url': resource.get('url'),
            'package_id': package_id or resource.get('package_id'),
            'force': force,
            'api_key': context.get('apikey') or config.get('ckan.site_api_key')
        }
        
        # Soumission au datapusher plus
        response = submit_to_datapusher_plus(datapusher_plus_url, job_data)
        
        if response['success']:
            # Mise à jour du statut de la ressource
            update_resource_status(context, resource_id, 'submitted')
            
            return jsonify({
                'success': True,
                'message': 'Fichier soumis avec succès au datapusher plus',
                'job_id': response.get('job_id'),
                'resource_id': resource_id
            })
        else:
            return jsonify({
                'success': False,
                'error': response.get('error', 'Erreur lors de la soumission')
            }), 500
            
    except toolkit.NotAuthorized:
        return jsonify({
            'success': False,
            'error': 'Non autorisé'
        }), 403
    except Exception as e:
        log.error(f'Erreur lors de la soumission: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'Erreur interne: {str(e)}'
        }), 500


def submit_to_datapusher_plus(datapusher_url, job_data):
    """
    Soumet un job au datapusher plus
    
    Args:
        datapusher_url (str): URL du service datapusher plus
        job_data (dict): Données du job à soumettre
        
    Returns:
        dict: Réponse avec success, job_id ou error
    """
    try:
        # URL de l'endpoint datapusher plus
        submit_url = f"{datapusher_url.rstrip('/')}/job"
        
        # Headers pour la requête
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'CKAN DatapusherPlusAPI'
        }

        log.debug(f'Envoi de la requête au datapusher plus: {submit_url}')
        log.debug(f'Données du job: {job_data}')
        
        # Envoi de la requête
        response = requests.post(
            submit_url,
            json=job_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'success': True,
                'job_id': result.get('job_id'),
                'message': result.get('message', 'Job soumis avec succès')
            }
        else:
            log.error(f'Erreur datapusher plus: {response.status_code} - {response.text}')
            return {
                'success': False,
                'error': f'Erreur HTTP {response.status_code}: {response.text}'
            }
            
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Timeout lors de la connexion au datapusher plus'
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': 'Impossible de se connecter au datapusher plus'
        }
    except Exception as e:
        log.error(f'Erreur lors de la soumission au datapusher plus: {str(e)}')
        return {
            'success': False,
            'error': f'Erreur: {str(e)}'
        }


def update_resource_status(context, resource_id, status):
    """
    Met à jour le statut de traitement d'une ressource
    
    Args:
        context (dict): Contexte CKAN
        resource_id (str): ID de la ressource
        status (str): Nouveau statut
    """
    try:
        # Récupération de la ressource actuelle
        resource = toolkit.get_action('resource_show')(
            context, {'id': resource_id}
        )
        
        # Mise à jour du statut
        resource['datapusher_plus_status'] = status
        resource['datapusher_plus_submitted'] = h.date_str_to_datetime('now').isoformat()
        
        # Sauvegarde
        toolkit.get_action('resource_update')(context, resource)
        
        log.info(f'Statut de la ressource {resource_id} mis à jour: {status}')
        
    except Exception as e:
        log.error(f'Erreur lors de la mise à jour du statut: {str(e)}')


@datapusherplusapi.route('/datapusher_plus_status/<resource_id>', methods=['GET'])
def datapusher_plus_status(resource_id):
    """
    Récupère le statut de traitement d'une ressource
    
    Args:
        resource_id (str): ID de la ressource
        
    Returns:
        JSON avec le statut de traitement
    """
    try:
        context = {'user': toolkit.c.user}
        
        # Vérification que la ressource existe
        try:
            resource = toolkit.get_action('resource_show')(
                context, {'id': resource_id}
            )
        except toolkit.ObjectNotFound:
            return jsonify({
                'success': False,
                'error': f'Ressource {resource_id} non trouvée'
            }), 404
        
        # Récupération du statut
        status = resource.get('datapusher_plus_status', 'unknown')
        submitted = resource.get('datapusher_plus_submitted')
        
        return jsonify({
            'success': True,
            'resource_id': resource_id,
            'status': status,
            'submitted': submitted,
            'resource_url': resource.get('url')
        })
        
    except Exception as e:
        log.error(f'Erreur lors de la récupération du statut: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'Erreur interne: {str(e)}'
        }), 500
