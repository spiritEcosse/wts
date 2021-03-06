"""
Flask app.

Import all models.
"""
from wts.settings import PROJECT
from wts.utils import create_app, create_db, create_migrate, import_models

app = create_app(name=PROJECT)
db = create_db(app)
migrate = create_migrate(app, db)

import_models(apps_folder='apps')
