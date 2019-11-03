import random

from docker_api_testing.docker_api_handler import DockerAPIHandler

def generate_random_id():
    """Generate a random Docker ID"""
    id_length = 64
    return ''.join(random.choice('0123456789abcdef') for i in range(id_length))

def get_nonexistent_container_id():
    """Find an ID that does not exist in our Docker containers"""
    api_handler = DockerAPIHandler()

    # Get all the container IDs
    endpoint = 'containers/json?all=true'
    response = api_handler.request('get', endpoint, None)
    if response.status_code != 200:
        error = 'Getting all Docker containers failed. Error: ' + response.text
        raise(ValueError(error))
    container_ids = [x['Id'] for x in response.json()]

    # Generate an ID that doesn't exist in our current container list
    random_id = generate_random_id()
    while random_id in container_ids:
        random_id = generate_random_id()
    return random_id
