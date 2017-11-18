# /instance/config.py

import sqlalchemy
import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    CONN = sqlalchemy.create_engine('sqlite:///test.db')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

#Only use dev config for now
app_config = {
    'development': DevelopmentConfig
}