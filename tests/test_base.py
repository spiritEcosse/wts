import pytest

mod = __import__('apps')


@pytest.mark.db
def test_all(factory):
    factory.run()

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
