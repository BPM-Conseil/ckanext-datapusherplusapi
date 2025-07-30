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
    url_prefix='/api/action'
)


def get_blueprints():
    """Returns the list of blueprints"""
    return [datapusherplusapi]


@datapusherplusapi.route('/datapusher_plus_submit', methods=['POST'])
def datapusher_plus_submit():
    """
    REST API to submit a file to datapusher plus
    
    Expected parameters:
    - resource_id: CKAN resource ID
    - force: Force submission even if already in progress (optional, default: False)
    
    Returns:
    - success: True/False
    - message: Status message
    """
    try:
        # Authentication check
        context = {'user': toolkit.c.user}
        toolkit.check_access('resource_update', context)
        
        # Get parameters
        data = request.get_json() or {}
        resource_id = data.get('resource_id')
        force = data.get('force', False)
        
        if not resource_id:
            return jsonify({
                'success': False,
                'error': 'resource_id is required'
            }), 400
        
        # Check that the resource exists
        try:
            resource = toolkit.get_action('resource_show')(
                context, {'id': resource_id}
            )
        except toolkit.ObjectNotFound:
            return jsonify({
                'success': False,
                'error': f'Resource {resource_id} not found'
            }), 404
        
        # Prepare data for datapusher plus
        job_data = {
            'resource_id': resource_id
        }
        
        # Add force only if True
        if force:
            job_data['force'] = force
            
        # Add API key if available
        api_key = context.get('apikey') or config.get('ckan.site_api_key')
        if api_key:
            job_data['api_key'] = api_key
        
        # Submit to datapusher plus
        response = submit_to_datapusher_plus(job_data)
        
        if response['success']:            
            return jsonify({
                'success': True,
                'message': 'File submitted successfully to datapusher plus',
                'resource_id': resource_id
            })
        else:
            return jsonify({
                'success': False,
                'error': response.get('error', 'Error during submission')
            }), 500
            
    except toolkit.NotAuthorized:
        return jsonify({
            'success': False,
            'error': 'Unauthorized'
        }), 403
    except Exception as e:
        log.error(f'Error during submission: {str(e)}')
        return jsonify({
            'success': False,
            'error': f'Internal error: {str(e)}'
        }), 500


def submit_to_datapusher_plus(job_data):
    """
    Submit a job to datapusher plus using CKAN action directly
    
    Args:
        job_data (dict): Job data to submit
        
    Returns:
        dict: Response with success, job_id or error
    """
    try:
        resource_id = job_data.get('resource_id')
        force = job_data.get('force', False)
        
        # Context for CKAN action
        context = {
            'ignore_auth': True,  # Ignore auth as already verified in the view
            'user': toolkit.c.user
        }
        
        # Parameters for datapusher action
        data_dict = {
            'resource_id': resource_id
        }
        
        # Add force if necessary
        if force:
            data_dict['force'] = force
            
        log.info(f'Submitting resource {resource_id} to datapusher via CKAN action')
        log.debug(f'Parameters: {data_dict}')
        
        # Direct call to CKAN datapusher_submit action
        try:
            result = toolkit.get_action('datapusher_submit')(context, data_dict)
            
            log.info(f'Resource {resource_id} successfully submitted to datapusher')
            log.debug(f'datapusher_submit action result: {result} (type: {type(result)})')
            
            # The datapusher_submit action can return a bool or a dict
            if isinstance(result, bool):
                # If it's a boolean, create an appropriate response
                if result:
                    return {
                        'success': True,
                        'job_id': f'datapusher-{resource_id}',
                        'message': 'Resource successfully submitted to datapusher plus',
                        'result': {'submitted': True}
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Datapusher submission failed'
                    }
            elif isinstance(result, dict):
                # If it's a dictionary, use the returned data
                return {
                    'success': True,
                    'job_id': result.get('job_id', f'datapusher-{resource_id}'),
                    'message': 'Resource successfully submitted to datapusher plus',
                    'result': result
                }
            else:
                # Unexpected case
                return {
                    'success': True,
                    'job_id': f'datapusher-{resource_id}',
                    'message': 'Resource successfully submitted to datapusher plus',
                    'result': {'raw_result': str(result)}
                }
            
        except toolkit.ValidationError as e:
            log.error(f'Validation error during submission: {e.error_dict}')
            return {
                'success': False,
                'error': f'Validation error: {", ".join([f"{k}: {v}" for k, v in e.error_dict.items()])}'
            }
            
        except toolkit.ObjectNotFound as e:
            log.error(f'Resource not found: {str(e)}')
            return {
                'success': False,
                'error': f'Resource not found: {str(e)}'
            }
            
        except toolkit.NotAuthorized as e:
            log.error(f'Not authorized for datapusher submission: {str(e)}')
            return {
                'success': False,
                'error': f'Not authorized: {str(e)}'
            }
            
    except Exception as e:
        log.error(f'Error during datapusher submission: {str(e)}')
        return {
            'success': False,
            'error': f'Internal error: {str(e)}'
        }
