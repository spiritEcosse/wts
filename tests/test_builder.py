from bs4 import BeautifulSoup as Bs

import pytest
from apps.html.builder import Builder


@pytest.mark.db
def test_builder(case):
    url = 'http://web/{}/'.format(case.id)
    builder = Builder(bs_input=url)
    builder.run()
    assert builder.prettify() == Bs(
        case.expected['res'], "html.parser"
    ).prettify()
