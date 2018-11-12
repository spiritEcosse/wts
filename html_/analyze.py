
from wts import settings
from wts.decorators import check_base


class Analyze:
    def is_alert(self):
        pass

    @classmethod
    @check_base(class_='badge', tags=('a', 'span', ))
    def is_badge(cls, html):
        pass

    def is_breadcrumb(self):
        pass

    def is_button(self):
        pass

    def is_button_group(self):
        pass

    def is_card(self):
        pass

    def is_carousel(self):
        pass

    def is_dropdown(self):
        pass

    def is_form(self):
        pass

    def is_input_group(self):
        pass

    def is_jumbotron(self):
        pass

    def is_list_group(self):
        pass

    def is_modal(self):
        pass

    def is_nav(self):
        pass

    def is_navbar(self):
        pass

    def is_pagination(self):
        pass

    def is_popover(self):
        pass

    def is_progres(self):
        pass

    def is_scrollspy(self):
        pass

    def is_tooltip(self):
        pass
