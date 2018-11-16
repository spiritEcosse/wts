"""
Flask app.

Import all models.
"""

import importlib
import os

from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

APPS_FOLDER = 'apps'
FILE_MODELS = 'models.py'


def import_models():
    """
    Import crutch for models.

    Recursively import all models.py from apps.
    """
    def replace(path): return path.replace(os.sep, '.')

    def split(path): return replace(os.path.splitext(path)[0])

    def join(di, file_): return split(os.path.join(di, file_))

    def imm(di, file_): return importlib.import_module(join(di, file_))

    [imm(di, file_) for di, dirs, files in os.walk(APPS_FOLDER)
     for file_ in files if file_ == FILE_MODELS]


import_models()
