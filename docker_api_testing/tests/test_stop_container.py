from unittest.mock import patch
from requests.exceptions import ConnectionError

from docker_api_testing.tests.docker_api_test_case import DockerAPITestCase
from docker_api_testing import config
from docker_api_testing.utilities import get_nonexistent_container_id

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

    def test_stop_nonexistent_container(self):
        container_id = get_nonexistent_container_id()
        endpoint = 'containers/{}/stop'.format(container_id)
        response = self.request('post', endpoint)
        self.assertEqual(response.status_code, 404)

'''
Additional tests that we could add in the future:
* Set the t parameter, and check before and after t seconds later to check if
  the container was stopped after a specific delay time
'''
