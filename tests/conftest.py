"""
config for pytest.

create app, initial_data.
"""

import os

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
    exp = 'expected'

    def __init__(self, case, func=None):
        self.case = case
        self.func = func
        self.is_model = hasattr(case.klass, '__table__')

        if self.is_model:
            self.obj = case.klass()

            for rel in self.obj.relf():
                value = self.case.input.pop(
                    rel.key) if rel.key in self.case.input else None

                if isinstance(value, list):
                    if all(map(lambda val: isinstance(val, dict), value)):
                        setattr(self.obj, rel.key, self.obj.rel(rel, value))

            for field, value in self.case.input.items():
                setattr(self.obj, field, value)
            # self.save_obj()
        else:
            self.obj = case.klass(**case.input)

    def event(self):
        getattr(self, 'event_{}'.format(self.case.event))()

    def event_set(self):
        for attr in self.exp_keys_set():
            assert getattr(self.obj, attr) == self.case.expected[attr]

    def exp_keys_set(self):
        return set(self.case.expected.keys())

    def save_obj(self):
        self.obj.save()

    def scope_func(self):
        if self.is_model:
            self.save_obj()
        self.assert_func()

    def assert_obj_model_param(self):
        self.save_obj()
        obj_keys = set(map(lambda val: val.key, self.obj.relf()))

        for attr in self.exp_keys_set().intersection(obj_keys):
            assert \
                [rel_obj.to_dict(['name']) for rel_obj in
                 getattr(self.obj, attr)] == self.case.expected[attr]

        for attr in self.exp_keys_set().difference(obj_keys):
            assert getattr(self.obj, attr) == self.case.expected[attr]

    def scope_obj_model(self):
        if self.case.event is None:
            self.assert_obj_model_param()
        else:
            self.event()

    def assert_obj_param(self):
        for key, value in self.case.expected.items():
            base_obj = self.obj

            for base_attr in key.split(os.extsep):
                base_obj = getattr(base_obj, base_attr)

            if isinstance(value, dict):
                if 'type' in value:
                    assert isinstance(base_obj, value['type'])
            else:
                assert base_obj == value

    def scope_obj(self):
        if self.is_model:
            self.scope_obj_model()
        else:
            self.assert_obj_param()

    def run(self):
        if self.func:
            self.scope_func()
            if not self.is_model:
                self.obj.driver.close()
                self.obj.driver.quit()
        else:
            self.scope_obj()

    def assert_func(self):
        if isinstance(self.func, str):
            assert callable(getattr(self.obj, self.func)) is True
        elif isinstance(self.func, dict):
            for key, values in self.func.items():
                base_obj = self.obj

                for base_attr in key.split(os.extsep):
                    base_obj = getattr(base_obj, base_attr)

                func = base_obj
                assert func() == values[self.exp]


def pytest_generate_tests(metafunc):
    func = metafunc.function

    if hasattr(func, 'db'):
        cases = []

        for case in Case.query.filter_by(name=func.__name__):
            if case.expected:
                factory = Factory(case)
                cases.append(factory)

            for func in case.func or []:
                factory = Factory(case, func=func)
                cases.append(factory)

        metafunc.parametrize("factory", cases)
