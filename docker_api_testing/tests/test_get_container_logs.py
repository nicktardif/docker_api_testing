from unittest.mock import patch
from requests.exceptions import ConnectionError

from docker_api_testing.tests.docker_api_test_case import DockerAPITestCase
from docker_api_testing import config
from docker_api_testing.utilities import get_nonexistent_container_id

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

    def test_get_logs_from_nonexistent_container(self):
        container_id = get_nonexistent_container_id()
        endpoint = 'containers/{}/logs?stdout=true&stderr=false'.format(
                container_id)
        response = self.request('get', endpoint)
        self.assertEqual(response.status_code, 404)

'''
Additional tests that we could add in the future:
* Enable timestamps and do a check that the output timestamps are within an
  expected range
* Set different tail values and check how many logs are returned. Possible
  values, [-1, 0, 1, 2, 10, 1000]
* Dynamically trigger logs during the test. This could be possible with an
  Nginx container (as a suggestion). With this, we'd be able to test the
  "since" and "until" keywords very easily
'''
