import json

from docker_api_testing.tests.docker_api_test_case import DockerAPITestCase

def parse_logs(response):
    """ Parse the Docker logs into just the text output"""
    lines = response.text.split('\n')

    # Skip the first 8 bytes of the log stream
    # Byte format documentation
    # https://docs.docker.com/engine/api/v1.40/#operation/ContainerAttach
    header_removed_output = [s[8:] for s in lines]

    empty_lines_removed = list(filter(None, header_removed_output))
    return empty_lines_removed

class LifecycleTest(DockerAPITestCase):
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

    def test_lifecycle(self):
        # Starts a container
        endpoint = 'containers/{}/start'.format(self.container_id)
        response = self.request('post', endpoint)
        self.assertEqual(response.status_code, 204)

        # Try to start the started container
        endpoint = 'containers/{}/start'.format(self.container_id)
        response = self.request('post', endpoint)
        self.assertEqual(response.status_code, 304)

        # Get the stdout logs
        expected_logs = ['hello stdout']
        endpoint = 'containers/{}/logs?stdout=true&stderr=false'.format(
                self.container_id)
        response = self.request('get', endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(parse_logs(response), expected_logs)

        # Get the stderr logs
        expected_logs = ['hello stderr']
        endpoint = 'containers/{}/logs?stdout=false&stderr=true'.format(
                self.container_id)
        response = self.request('get', endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(parse_logs(response), expected_logs)

        # Get all the logs
        # NOTE: stderr is always output before stdout in this case?
        expected_logs = ['hello stderr', 'hello stdout']
        endpoint = 'containers/{}/logs?stdout=true&stderr=true'.format(
                self.container_id)
        response = self.request('get', endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(parse_logs(response), expected_logs)

        # Stop the container
        endpoint = 'containers/{}/stop'.format(self.container_id)
        response = self.request('post', endpoint)
        self.assertEqual(response.status_code, 204)

        # Try to stop the stopped container
        endpoint = 'containers/{}/stop'.format(self.container_id)
        response = self.request('post', endpoint)
        self.assertEqual(response.status_code, 304)
