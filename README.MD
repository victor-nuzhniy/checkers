# Online game checkers

## Description
    This game created with Python using Django, with channels socket solution.
    

## Installation

### Sensitive data
    .env file must be created locally and filled with sensitive info:
        - SECRET_KEY
        - MAIL_USERNAME
        - MAIL_PASSWORD
        - MAIL_FROM
        - MAIL_PORT
        - MAIL_SERVER

### As a package manager used Poetry. 
        Poetry install ...

### Redis
    We will use a channel layer that uses Redis as its backing store. 
    To start a Redis server on port 6379, run the following command:
        docker run -p 6379:6379 -d redis:5
