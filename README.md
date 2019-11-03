# Docker API Testing
This Python project tests parts of the Docker Container API, specifically the Start Container, Get Container Logs, and Stop Container API calls.

## System Dependencies
* Ubuntu 18.04 OS
* Docker 18.09.7+
    * Installation instructions [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
* This testing suite was built with the Docker API 1.40 documentation [link](https://docs.docker.com/engine/api/v1.40/)

### Pipenv
Pipenv is what we use to manage our Python dependencies. You can choose to install this in user space or globally on your system.
```
# Install dependencies so we can install and use pipenv
apt install python-pip python3-distutils

# Install pipenv (user space)
pip install --user pipenv
# NOTE: Need to add ~/.local/bin to your PATH variable if you do a user install

# OR - you can install pipenv into global space
pip install pipenv
```

## Running
```
# Make sure the Python package dependencies are installed
pipenv install

# Run the API tests
pipenv run python run_tests.py
```

These tests assume that the Docker daemon is running on your system and is available via a Unix socket at `/var/run/docker.sock`. If this is not the case, the tests will fail.

In specific tests we simulate the Docker daemon being down by setting the query Unix socket to `/var/run/docker2.sock`, and these check for the expected connection errors.
