import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////wts/app.db'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////wts/app.db'
    SQLALCHEMY_BINDS = {
        'test_cases':         'sqlite:////wts/tests/test_cases.db',
    }


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_BINDS = {
        'test_cases':         'sqlite:////wts/tests/test_cases.db',
    }
