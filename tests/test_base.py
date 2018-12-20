import pytest

mod = __import__('apps')


@pytest.mark.db
def test_all(factory):
    try:
        factory.run()
    except Exception as er:
        print(self.case.id)
        raise er


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
