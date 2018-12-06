from sqlalchemy.orm import object_mapper, properties

import pytest

mod = __import__('apps')


@pytest.mark.db
def test_all(case):
    klass = getattr(mod, case.klass)

    obj = klass()
    rel_props = list(filter(
        lambda p: isinstance(p, properties.RelationshipProperty),
        object_mapper(obj).iterate_properties
    ))

    for rel_prop in rel_props:
        value = case.input.pop(
            rel_prop.key
        ) if rel_prop.key in case.input else None

        if type(value) is list:
            if all(map(lambda val: type(val) is dict, value)):
                setattr(obj, rel_prop.key, obj.rel(rel_prop, value))

    for field, value in case.input.items():
        setattr(obj, field, value)

    exp_keys = set(case.expected.keys())
    obj_keys = set(map(lambda val: val.key, rel_props))

    if case.event == 'set':
        for attr in exp_keys:
            assert getattr(obj, attr) == case.expected[attr]
    else:
        obj.save()

        for attr in exp_keys.intersection(obj_keys):
            assert \
                [rel_obj.to_dict(['name']) for rel_obj in getattr(obj, attr)] \
                == case.expected[attr]

        for attr in exp_keys.difference(obj_keys):
            assert getattr(obj, attr) == case.expected[attr]

# @pytest.mark.db
# def test_all(case):
#     klass = mod.getattr(case.klass)
#     # check attr
#
#     # if case have list func , check their in сycle
#
#
# class FactoryDef:
#     pass
