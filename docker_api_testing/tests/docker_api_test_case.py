import json

from unittest import TestCase
from docker_api_testing.docker_api_handler import DockerAPIHandler
from docker_api_testing import config

class DockerAPITestCase(TestCase):
    container_id = None

    def setUp(self):
        """Pulls a small image and creates a container"""
        # Pulls an image (alpine is a nice small image)
        image_name = 'alpine'
        endpoint = 'images/create?fromImage={}&tag=latest'.format(image_name)
        response = self.request('post', endpoint)
        self.assertEqual(response.status_code, 200)

        # Creates a container
        endpoint = 'containers/create'
        data = {
            'Image': image_name,
            'Cmd': ['sh', '-c', 'echo hello stdout; >&2 echo hello stderr'],
        }
        response = self.request('post', endpoint, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
        self.container_id = response.json()['Id']

    def tearDown(self):
        """Deletes created container after tests finish"""
        # If anything failed, ensure that the container is stopped first
        endpoint = 'containers/{}/stop'.format(self.container_id)
        response = self.request('post', endpoint)

        endpoint = 'containers/{}'.format(self.container_id)
        response = self.request('delete', endpoint)

    def request(self, action, endpoint, data=None):
        """Wraps Docker HTTP requests"""
        api_handler = DockerAPIHandler()
        return api_handler.request(action, endpoint, data)
