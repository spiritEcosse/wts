"""
config for pytest.

create app, initial_data.
"""

import pytest
from app import app as core_app
from app import db
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


class Factory:

    def __init__(self, case, func_name=None):
        self.case = case
        self.func_name = func_name
        self.obj = case.klass()

        for rel in self.obj.relf():
            value = self.case.input.pop(
                rel.key) if rel.key in self.case.input else None

            if isinstance(value, list):
                if all(map(lambda val: isinstance(val, dict), value)):
                    setattr(self.obj, rel.key, self.obj.rel(rel, value))

        for field, value in self.case.input.items():
            setattr(self.obj, field, value)

    def event(self):
        getattr(self, 'event_{}'.format(self.case.event))()

    def event_set(self):
        for attr in self.exp_keys_set():
            assert getattr(self.obj, attr) == self.case.expected[attr]

    def exp_keys_set(self):
        return set(self.case.expected.keys())

    def run(self):
        if self.func_name:
            self.obj.save()
            self.func()
        else:
            obj_keys = set(map(lambda val: val.key, self.obj.relf()))

            if self.case.event is not None:
                self.event()
            else:
                self.obj.save()

                for attr in self.exp_keys_set().intersection(obj_keys):
                    assert \
                        [rel_obj.to_dict(['name']) for rel_obj in
                         getattr(self.obj, attr)] == self.case.expected[attr]

                for attr in self.exp_keys_set().difference(obj_keys):
                    assert getattr(self.obj, attr) == self.case.expected[attr]

    def func(self):
        assert callable(getattr(self.obj, self.func_name)) is True

    def get_func(self):
        return self.case.input.get('func', [])


def pytest_generate_tests(metafunc):
    func = metafunc.function

    if hasattr(func, 'db'):
        cases = []

        for case in Case.query.filter_by(name=func.__name__):
            factory = Factory(case)
            cases.append(factory)

            for func in factory.get_func():
                if isinstance(func, str):
                    factory = Factory(case, func_name=func)
                    cases.append(factory)

        metafunc.parametrize("factory", cases)
