"""
config for pytest.

create app, initial_data.
"""

import pytest
from app import app as core_app
from app import db
from apps.css.models import Property, Value
from apps.html.models import Classes
from apps.test.models import Case
from wts.config import TestingConfig


@pytest.fixture
def app():
    """
    Flask app import from real app.

    Will be use TestingConfig from APP_SETTINGS.

    With context, order:
        Creates all tables.
        Perform our tasks.
        Session remove.
        Drop all tables.
    """
    core_app.config['SQLALCHEMY_DATABASE_URI'] = \
        TestingConfig.SQLALCHEMY_DATABASE_URI

    with core_app.app_context():
        db.create_all(bind=None)
        db.session.expunge_all()
        db.session.commit()
        yield core_app
        db.session.remove()  # looks like db.session.close() would work as well
        db.drop_all(bind=None)


@pytest.fixture
def initial_data(app):
    """Fixture initial data."""
    # pr = Property(name='display').save()
    # Value(name='block', property=pr, inline=False).save()
    # Value(name='inline', property=pr, block=False).save()
    # Value(name='inline-block', property=pr).save()
    # [
    #     Classes(name=name).save()
    #     for name in ['card', "card-body", "card-title", "card-text",
    #                  "bg-primary", "border-none", "row", "text-center",
    #                  "text-white", "col-5", "col-7",
    #                  "align-self-center"]
    # ]
    #
    # border = Property(name='border').save()
    # Classes(name='card', properties=[border]).save()


def pytest_generate_tests(metafunc):
    func = metafunc.function

    if hasattr(func, 'db'):
        metafunc.parametrize(
            "case", [case for case in Case.query.filter_by(name=func.__name__)]
        )
