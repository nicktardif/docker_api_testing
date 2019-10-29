from requests.exceptions import ConnectionError
import requests_unixsocket

from docker_api_testing import config

class DockerAPIHandler():
    """Handles all web requests to the Docker API"""
    def __init__(self):
        self.session = requests_unixsocket.Session()

    def get(self, endpoint, data):
        try:
            return self.session.get(
                    config.docker_socket + config.docker_version + endpoint,
                    data=data)
        except ConnectionError as e:
            print('Error: Could not establish connection to Docker daemon')
        return None

    def post(self, endpoint, data):
        try:
            headers = {'Content-type': 'application/json'}
            return self.session.post(
                    config.docker_socket + config.docker_version + endpoint,
                    data=data,
                    headers=headers,)
        except ConnectionError as e:
            print('Error: Could not establish connection to Docker daemon')
        return None

    def delete(self, endpoint, data):
        try:
            return self.session.delete(
                    config.docker_socket + config.docker_version + endpoint,
                    data=data,)
        except ConnectionError as e:
            print('Error: Could not establish connection to Docker daemon')
        return None
