from requests.exceptions import ConnectionError
import requests_unixsocket

from docker_api_testing import config

class DockerAPIHandler():
    """Handles all web requests to the Docker API"""
    def __init__(self):
        self.session = requests_unixsocket.Session()

    def request(self, action, endpoint, data=None):
        """Make web request to the Docker API"""
        possible_actions = ['get', 'post', 'delete']
        if action not in possible_actions:
            raise ValueError('action "{}" not valid. Options: {}'.format(
                action,
                ' '.join(possible_actions)))

        http_methods = {
            'get': self.session.get,
            'post': self.session.post,
            'delete': self.session.delete,
        }

        # Attempt the web request
        headers = {'Content-type': 'application/json'}
        return http_methods[action](
                config.docker_socket + config.docker_version + endpoint,
                data=data,
                headers=headers,)
