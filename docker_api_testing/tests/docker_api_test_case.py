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
        response = api_handler.request(action, endpoint, data)

        # Gracefully handle any connection errors
        if response is None:
            error = 'Docker daemon was not found at ' + config.docker_socket
            self.fail(error)
        return response
