import os
import datetime

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"options": "-csearch_path=dev"}}
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    JWT_VERIFY_SUB = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=120)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Get config by name
config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
