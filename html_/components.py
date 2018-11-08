import sys
from collections import OrderedDict

from bs4 import BeautifulSoup

from html_.base import *


class Components:
    def make_alert(self):
        pass

    @classmethod
    def make_badge(cls, attr=(), text=''):
        attr = OrderedDict(attr)
        attr['class'] = 'badge ' + attr.get('class', 'badge-primary')
        return str(a(attr, text)) if attr.get('href', '') else str(span(attr, text))

    @classmethod
    def breadcrumb(cls, items=(), attr=(), **kwargs):
        name = kwargs['name']
        attr = OrderedDict(attr)
        attr['aria-label'] = name
        html = nav(attr)
        html_ol = ol(OrderedDict((('class', name), )))

        for item in items[:-1]:
            attr_li = OrderedDict(
                (
                    ('class', name + '-item'),
                )
            )
            attr_a = OrderedDict(
                (
                    ('href', '#'),
                )
            )

            html_ol <= li(attr_li) <= a(attr_a, item)

        attr_li = OrderedDict(
            (
                ('class', name + '-item active'),
                ('aria-current', 'page'),
            )
        )
        html_ol <= li(attr_li, items[-1] if items else '')
        html <= html_ol
        return BeautifulSoup(str(html), "html.parser").prettify()

    def make_button(self):
        pass

    def make_button_group(self):
        pass

    def make_card(self):
        pass

    def make_carousel(self):
        pass

    def make_dropdown(self):
        pass

    def make_form(self):
        pass

    def make_input_group(self):
        pass

    def make_jumbotron(self):
        pass

    def make_list_group(self):
        pass

    def make_modal(self):
        pass

    def make_nav(self):
        pass

    def make_navbar(self):
        pass

    def make_pagination(self):
        pass

    def make_popover(self):
        pass

    def make_progres(self):
        pass

    def make_scrollspy(self):
        pass

    def make_tooltip(self):
        pass
