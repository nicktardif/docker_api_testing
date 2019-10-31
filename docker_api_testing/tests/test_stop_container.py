from unittest.mock import patch
from requests.exceptions import ConnectionError

from docker_api_testing.tests.docker_api_test_case import DockerAPITestCase
from docker_api_testing import config

class StopContainerTest(DockerAPITestCase):
    @patch('docker_api_testing.config.docker_socket', config.fake_socket)
    def test_missing_daemon(self):
        """Test stopping a container with an invalid socket"""
        with self.assertRaises(ConnectionError):
            endpoint = 'containers/{}/stop'.format(self.container_id)
            self.request('post', endpoint)

    def test_invalid_request(self):
        endpoint = 'containers/{}/stop'.format(self.container_id)
        response = self.request('get', endpoint)
        self.assertEquals(response.status_code, 404)

    # Note: This may be the same test as stopping a stopped container.
    # Not sure if there is a difference between stopping a container that
    # never started, and stopping an already stopped container.
    def test_stop_unstarted_container(self):
        endpoint = 'containers/{}/stop'.format(self.container_id)
        response = self.request('post', endpoint)
        self.assertEquals(response.status_code, 304)

    # TODO: Attempt to stop a nonexistent container
