from html.base import *
from collections import OrderedDict

class Components:
    @classmethod
    def make_badge(cls, attr=(), text=''):
        attr = OrderedDict(attr)
        attr['class'] = 'badge ' + attr.get('class', 'badge-primary')
        return str(a(attr, text)) if attr.get('href', '') else str(span(attr, text))

    def make_alert(self):
        pass

    def make_breadcrumb(self):
        pass

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
