"""Settings for checkers project with daphne production routing."""
from config.settings import *  # noqa: F401,F403

ASGI_APPLICATION = "deploy_config.asgi.application"
