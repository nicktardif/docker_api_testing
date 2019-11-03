from docker_api_testing.tests.docker_api_test_case import DockerAPITestCase

endpoint = 'info'

class ApiHandlerTest(DockerAPITestCase):
    """Tests that the API Handler sends requests as expected. Does NOT
    test Docker API responses"""

    def test_valid_get_request(self):
        response = self.request('get', endpoint)

    def test_valid_post_request(self):
        response = self.request('post', endpoint)

    def test_valid_delete_request(self):
        response = self.request('delete', endpoint)

    def test_invalid_put_request(self):
        """Checks that the APIHandler throws an exception on unimplemented
        HTTP actions"""
        http_action = 'put'
        possible_api_endpoints = 'get post delete'
        expected_error_message = 'action "{}" not valid. Options: {}'.format(
                http_action,
                possible_api_endpoints)
        with self.assertRaisesRegex(ValueError, expected_error_message):
            response = self.request(http_action, endpoint)
