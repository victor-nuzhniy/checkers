# Online game checkers

## Description
    This game created with Python using Django, with channels socket solution.
    

## Installation

### Sensitive data

    .env file must be created locally and filled with sensitive info:
        - SECRET_KEY - django secret key
        - POSTGRES_HOST - postgres section
        - POSTGRES_PORT
        - POSTGRES_USER
        - POSTGRES_PASSWORD
        - POSTGRES_DB
        - MAIL_USERNAME - smtp server settings
        - MAIL_PASSWORD
        - MAIL_FROM
        - MAIL_PORT
        - MAIL_SERVER
        - DJANGO_SUPERUSER_USERNAME - django superuser data 
        - DJANGO_SUPERUSER_EMAIL
        - DJANGO_SUPERUSER_PASSWORD
        - ALLOWED_HOSTS - django settings allowed hosts
        - DEBUG - django settings debug mode
        - REDIS_LOCATION - redis data
        - CHANNELS_HOST
        - CHANNERLS_PORT


### Run the project with the command

    docker-compose up

### Nginx configuration

    For now is for local usage. Project will be accessible at 127.0.0.1 after running.
    Change server name with deployed host name on.

### SSL settings

    Add ssl django settings in deploy_config.settings module, leave config.settings for
    local running with python manage.py runserver

### Deployment

    You should change directives in docker-compose postgres and redis services ports to 
    expose or restrict access to pointed ports with third party libraries, for example,
    ufw-docker.

### Admin site

    After project starting with docker-compose an admin user will automatically be created
    with data from .env file.

### smtp server

    For user registration confirmation email message is used. Set proper stmp server settings 
    in .env file.


### Usage

    How to play described on first page.


