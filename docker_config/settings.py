"""Settings for checkers project with daphne production routing."""
from config.settings import *

ASGI_APPLICATION = "docker_config.asgi.application"
