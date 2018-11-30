import importlib
import os

from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from wts import settings


def create_app(obj=os.environ['APP_SETTINGS'], name=__name__):
    app = Flask(name)
    app.config.from_object(obj)
    return app


def create_db(app):
    return SQLAlchemy(app)


def create_migrate(app, db):
    return Migrate(app, db)


def import_models(apps_folder, file_models='models.py'):
    """
    Import crutch for models.

    Recursively import all models.py from apps.
    """
    def replace(path): return path.replace(os.sep, '.')

    def split(path): return replace(os.path.splitext(path)[0])

    def join(di, file_): return split(os.path.join(di, file_))

    def imm(di, file_): return importlib.import_module(join(di, file_))

    [imm(di, file_) for di, dirs, files in os.walk(apps_folder)
     for file_ in files if file_ == file_models]


def create_driver():
    return webdriver.Remote(
        command_executor=settings.REMOTE_DRIVER,
        desired_capabilities=settings.CAPABILITIES,
    )


def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)
