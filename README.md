# Docker API Testing Project
TODO: Fill in what this project does

## Dependencies
* Ubuntu 18.04 OS
* Docker 18.09.7+
    * Installation instructions [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
* This testing suite was built with the Docker API 1.40 documentation

Pipenv
```
# Install dependencies so we can install pipenv
apt install python-pip python3-distutils

# Install pipenv (user space)
pip install --user pipenv
# NOTE: Need to add ~/.local/bin to your PATH variable if you do a user install

# Or you can install pipenv into global space
pip install pipenv
```

## Running
```
# Make sure the dependencies are installed
pipenv install

# Run the API tests
pipenv run python run_tests.py
```
