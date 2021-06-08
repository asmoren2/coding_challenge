from unittest import mock, TestCase
from flask import Flask
from app.routes import app
from app.models import version_control_info

class IntegrationTest(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.app.testing = True

    def tearDown(self):
        self.app_context.pop()

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_health_check(self):
        response = self.app.get('/health-check')
        assert response.status_code == 200
        assert 'All Good!' in str(response.data)

    @mock.patch('app.routes.github_service.github_service')
    @mock.patch('app.routes.bitbucket_service.bitbucket_service')
    def test_version_control_info(self, mock1, mock2): 
        response_object_github = version_control_info.VSInfo(None, 'Github', 10, 1, 100, ['python', 'java'], ['CODE'])
        response_object_bitbucket = version_control_info.VSInfo('ERRRRR', 'Bitbucket', 1, 0, 1, None, None)
        mock1.return_value = (response_object_github)
        mock2.return_value = (response_object_bitbucket)

        response = self.app.get(
            '/api/v1/version-control-info?github_org=mailchimp&bitbucket_team=mailchimp',
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Bitbucket", str(response.data))
        self.assertIn("Github", str(response.data))
        self.assertIn("ERRRRR", str(response.data))




