import logging
from ckan.common import request, response, json, _
import ckan.logic as logic
import ckan.plugins.toolkit as toolkit

log = logging.getLogger(__name__)

class DatapusherAPIController:
    def relaunch(self):
        context = {'model': logic.model,
                   'session': logic.model.Session,
                   'user': toolkit.get_action('get_site_user')({'ignore_auth': True}, {})['name']}

        try:
            data = json.loads(request.body)
            resource_id = data.get('resource_id')

            if not resource_id:
                return toolkit.make_response({'success': False, 'error': 'Missing resource_id'}, 400)

            toolkit.get_action('resource_show')(context, {'id': resource_id})

            # Trigger DataPusher job
            toolkit.enqueue_job(
                toolkit.get_action('datapusher_submit'),
                [resource_id]
            )

            return toolkit.make_ok({'message': f'DataPusher relaunched for resource {resource_id}'})

        except logic.NotFound:
            return toolkit.make_response({'success': False, 'error': 'Resource not found'}, 404)
        except Exception as e:
            log.error(f"Error relaunching DataPusher: {e}")
            return toolkit.make_response({'success': False, 'error': str(e)}, 500)
