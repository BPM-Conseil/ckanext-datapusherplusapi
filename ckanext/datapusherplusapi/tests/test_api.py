# -*- coding: utf-8 -*-
"""
Tests pour l'API datapusher plus
"""
import json
import pytest
from unittest.mock import patch, Mock
from ckan.tests import helpers
from ckan.tests.factories import Resource, Dataset


class TestDatapusherPlusApi(helpers.FunctionalTestBase):
    """Tests pour l'API REST datapusher plus"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        helpers.reset_db()
        self.app = helpers._get_test_app()
    
    def test_submit_valid_resource(self):
        """Test de soumission d'une ressource valide"""
        # Création d'un dataset et d'une ressource de test
        dataset = Dataset()
        resource = Resource(
            package_id=dataset['id'],
            format='csv',
            url='http://example.com/data.csv'
        )
        
        # Mock de la réponse datapusher plus
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'job_id': 'test-job-123',
                'message': 'Job soumis avec succès'
            }
            mock_post.return_value = mock_response
            
            # Appel de l'API
            response = self.app.post(
                '/api/3/action/datapusher_plus_submit',
                data=json.dumps({'resource_id': resource['id']}),
                content_type='application/json',
                extra_environ={'REMOTE_USER': 'testsysadmin'}
            )
            
            # Vérifications
            assert response.status_code == 200
            data = json.loads(response.body)
            assert data['success'] is True
            assert 'job_id' in data
    
    def test_submit_missing_resource_id(self):
        """Test avec resource_id manquant"""
        response = self.app.post(
            '/api/3/action/datapusher_plus_submit',
            data=json.dumps({}),
            content_type='application/json',
            extra_environ={'REMOTE_USER': 'testsysadmin'},
            expect_errors=True
        )
        
        assert response.status_code == 400
        data = json.loads(response.body)
        assert data['success'] is False
        assert 'resource_id est requis' in data['error']
    
    def test_submit_nonexistent_resource(self):
        """Test avec une ressource inexistante"""
        response = self.app.post(
            '/api/3/action/datapusher_plus_submit',
            data=json.dumps({'resource_id': 'nonexistent-id'}),
            content_type='application/json',
            extra_environ={'REMOTE_USER': 'testsysadmin'},
            expect_errors=True
        )
        
        assert response.status_code == 404
        data = json.loads(response.body)
        assert data['success'] is False
        assert 'non trouvée' in data['error']
    
    def test_get_status_valid_resource(self):
        """Test de récupération du statut d'une ressource"""
        # Création d'une ressource de test
        dataset = Dataset()
        resource = Resource(
            package_id=dataset['id'],
            format='csv',
            url='http://example.com/data.csv',
            datapusher_plus_status='completed'
        )
        
        response = self.app.get(
            f'/api/3/action/datapusher_plus_status/{resource["id"]}',
            extra_environ={'REMOTE_USER': 'testsysadmin'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.body)
        assert data['success'] is True
        assert data['resource_id'] == resource['id']
        assert 'status' in data
    
    def test_unauthorized_access(self):
        """Test d'accès non autorisé"""
        response = self.app.post(
            '/api/3/action/datapusher_plus_submit',
            data=json.dumps({'resource_id': 'test-id'}),
            content_type='application/json',
            expect_errors=True
        )
        
        assert response.status_code == 403
        data = json.loads(response.body)
        assert data['success'] is False
        assert 'Non autorisé' in data['error']
