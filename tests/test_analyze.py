import pytest
from apps.css.models import Property, Value
from apps.html.analyze import Analyze

data_test = (
    # ({"display": "block", "width": 500}, False),  # 0
    # ({"display": "block", "width": 2000}, False),  # 1
    # ({"display": "inline", "width": 500}, True),  # 2
    # ({"display": "inline", "width": 2000}, True),  # 3
    # ({"display": "inline-block", "width": 500}, True),  # 4
    # ({"display": "inline-block", "width": 2000}, False),  # 5
    # ({"float": "left", "display": "block", "width": 500}, True),  # 6 !
    # ({"float": "left", "display": "block", "width": 2000}, False),  # 7
    # ({"float": "left", "display": "inline", "width": 500}, True),  # 8
    # ({"float": "left", "display": "inline", "width": 2000}, False),  # 9 !
    # ({"float": "left", "display": "inline-block", "width": 500}, True),  # 10
    # ({"float": "left", "display": "inline-block", "width": 2000}, False),  # 11
    # ({"float": "right", "display": "inline", "width": 2000}, False),  # 12 !
    # ({"float": "none", "display": "inline", "width": 2000}, True),  # 13 !
    # ({"float": "right", "display": "inline", "width": 500}, False),  # 14 !
    # ({"float": "right", "display": "block", "width": 500}, False),  # 15 !
    # ({"float": "right", "display": "block", "width": 2000}, False),  # 16
)

data_test_horizontal_center = (
    # ({"display": "flex"}, False),  # 0
    # ({"display": "block"}, False),  # 1
    # ({"display": "inline"}, False),  # 2
    # ({"display": "inline-block"}, False),  # 3
    # ({"display": "block", "justify-content": "center"}, False),  # 4
    # ({"justify-content": "center"}, False),  # 5
    # ({"display": "flex", "justify-content": "center"}, True),  # 6
    # ({"display": "flex", "justify-content": "flex-start"}, False),  # 7
    # ({"display": "flex", "justify-content": "flex-end"}, False),  # 8
    # ({"display": "flex", "justify-content": "space-between"}, False),  # 9
    # ({"display": "flex", "justify-content": "space-around"}, False),  # 10
    # ({"display": "flex", "justify-content": "initial"}, False),  # 11
    # ({"display": "inline", "justify-content": "center"}, False),  # 12
    # ({"display": "inline-block", "justify-content": "center"}, False),  # 13
    # ({"display": "flex", "text-align": "center"}, False),  # 14
    # ({"display": "block", "text-align": "center"}, True),  # 15
    # ({"display": "inline", "text-align": "center"}, True),  # 16
    # ({"display": "inline-block", "text-align": "center"}, True),  # 17
)

data_test_vertical_center = (
    # ({"align-self": "center"}, True),  # 0
    # ({"align-self": "auto"}, False),  # 1
    # ({"align-self": "stretch"}, False),  # 2
    # ({"align-self": "flex-start"}, False),  # 3
    # ({"align-self": "flex-end"}, False),  # 4
    # ({"align-self": "baseline"}, False),  # 5
    # ({"align-self": "initial"}, False),  # 6
    # ({"align-items": "center"}, True),  # 7
    # ({"align-items": "stretch"}, False),  # 8
    # ({"align-items": "flex-start"}, False),  # 9
    # ({"align-items": "flex-end"}, False),  # 10
    # ({"align-items": "baseline"}, False),  # 11
    # ({"align-items": "initial"}, False),  # 12
)


# class TestAnalyze:
#     @pytest.mark.parametrize("input,expected", data_test)
#     def test_append(self, input, expected):
#         input['value'] = Value.query.filter_by(
#             property=Property.query.filter_by(name='display').one(),
#             name=input['display']
#         ).one()
#
#         analyze = Analyze(**input)
#         assert analyze.append() == expected
#
#     @pytest.mark.parametrize("input,expected", data_test_horizontal_center)
#     def test_horizontal_center(self, input, expected):
#         analyze = Analyze(**input)
#         assert analyze.horizontal_center() == expected
#
#     @pytest.mark.parametrize("input,expected", data_test_vertical_center)
#     def test_vertical_center(self, input, expected):
#         analyze = Analyze(**input)
#         assert analyze.vertical_center() == expected
#

def test_initial_data():
    assert Property.query.count() == 1
    assert len(Property.query.first().values) == 3


@pytest.mark.db
def test_vertical_center(case):
    analyze = Analyze(case.input['css'])
    assert analyze.vertical_center() == case.expected['res']


@pytest.mark.db
def test_merge(case):
    analyze = Analyze(
        css=case.input.get('css', {}),
        html=case.input.get('html', '')
    )
    assert analyze.merge() == case.expected['res']
