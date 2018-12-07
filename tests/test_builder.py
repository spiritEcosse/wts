# from bs4 import BeautifulSoup as Bs
#
# import pytest
# from apps.html.builder import Builder
#
#
# @pytest.mark.db
# def test_builder(case):
#     from wts.utils import create_driver
#     import uuid
#     driver = create_driver()
#
#     path = '/wts/tests/tmp/{}.html'.format(str(uuid.uuid4()))
#     with open(path, "w") as f:
#         f.write('<div class="temp"></div>')
#     driver.get('file://{}'.format(path))

#     url = 'http://web/{}/'.format(case.id)
#     builder = Builder(bs_input=url)
#     builder.run()
#     assert builder.prettify() == Bs(
#         case.expected['res'], "html.parser"
#     ).prettify()
