import pytest
from apps.test.models import Case


@pytest.mark.db
def test_validate_input(case):
    obj = Case()
    obj.input = case.input
    assert obj.input['html'] == case.expected['res']

    obj = Case(input=case.input)
    assert obj.input['html'] == case.expected['res']
