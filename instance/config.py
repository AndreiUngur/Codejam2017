# /instance/config.py

import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    CONN = sqlalchemy.create_engine('sqlite:///test.db')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

#Only use dev config for now
app_config = {
    'development': DevelopmentConfig
}