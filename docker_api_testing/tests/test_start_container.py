from unittest.mock import patch
from requests.exceptions import ConnectionError

from docker_api_testing.tests.docker_api_test_case import DockerAPITestCase
from docker_api_testing import config
from docker_api_testing.utilities import get_nonexistent_container_id

class StartContainerTest(DockerAPITestCase):
    @patch('docker_api_testing.config.docker_socket', config.fake_socket)
    def test_missing_daemon(self):
        """Test starting a container with an invalid socket"""
        with self.assertRaises(ConnectionError):
            endpoint = 'containers/{}/start'.format(self.container_id)
            self.request('post', endpoint)

    def test_invalid_request(self):
        endpoint = 'containers/{}/start'.format(self.container_id)
        response = self.request('get', endpoint)
        self.assertEquals(response.status_code, 404)

    def test_start_nonexistent_container(self):
        container_id = get_nonexistent_container_id()
        endpoint = 'containers/{}/start'.format(container_id)
        response = self.request('post', endpoint)
        self.assertEqual(response.status_code, 404)

'''
Additional tests that we could add in the future:
* Set detachKeys parameter and check if we can detach from an interactive
  terminal using a different command sequence
'''
