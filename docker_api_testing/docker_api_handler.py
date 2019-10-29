from requests.exceptions import ConnectionError
import requests_unixsocket

from docker_api_testing import config

class DockerAPIHandler():
    """Handles all web requests to the Docker API"""
    def __init__(self):
        self.session = requests_unixsocket.Session()

    def get(self, endpoint, data):
        response = None
        try:
            response = self.session.get(
                    config.docker_socket + endpoint,
                    data=data)
        except ConnectionError as e:
            pass
        return response

    def post(self, endpoint, data):
        response = None
        try:
            headers = {'Content-type': 'application/json'}
            response = self.session.post(
                    config.docker_socket + endpoint,
                    data=data,
                    headers=headers,)
        except ConnectionError as e:
            pass
        return response

    def delete(self, endpoint, data):
        response = None
        try:
            response = self.session.delete(
                    config.docker_socket + endpoint,
                    data=data,)
        except ConnectionError as e:
            pass
        return response
