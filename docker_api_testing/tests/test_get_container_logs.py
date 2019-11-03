from unittest.mock import patch
from requests.exceptions import ConnectionError

from docker_api_testing.tests.docker_api_test_case import DockerAPITestCase
from docker_api_testing import config

class GetContainerLogsTest(DockerAPITestCase):
    @patch('docker_api_testing.config.docker_socket', config.fake_socket)
    def test_missing_daemon(self):
        """Test getting logs with an invalid socket"""
        with self.assertRaises(ConnectionError):
            endpoint = 'containers/{}/logs?stdout=true&stderr=false'.format(
                    self.container_id)
            self.request('get', endpoint)

    def test_invalid_request(self):
        endpoint = 'containers/{}/logs?stdout=true&stderr=false'.format(
                self.container_id)
        response = self.request('post', endpoint)
        self.assertEquals(response.status_code, 404)

    # TODO: Attempt to get logs from a nonexistent container
