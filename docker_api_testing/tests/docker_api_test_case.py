from unittest import TestCase
from docker_api_testing.docker_api_handler import DockerAPIHandler
from docker_api_testing import config

class DockerAPITestCase(TestCase):

    def request(self, action, endpoint, data=None):
        """Wraps Docker HTTP requests. Handles daemon connection errors"""
        possible_actions = ['get', 'post', 'delete']
        assert(action in possible_actions)

        # Make the request
        api_handler = DockerAPIHandler()
        response = None
        if action == 'get':
            response = api_handler.get(endpoint, data)
        if action == 'post':
            response = api_handler.post(endpoint, data)
        if action == 'delete':
            response = api_handler.delete(endpoint, data)

        # Gracefully handle any connection errors
        if response is None:
            error = 'Docker daemon was not found at ' + config.docker_socket
            self.fail(error)
        return response
