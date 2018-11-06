from html.components import Components
import pytest

class TestComponenets(object):
    @pytest.mark.parametrize("input,output", (
        ((), '<span class="badge badge-primary"></span>'),
        (
            ((('class', 'badge-success'), ), 'Text'),
            '<span class="badge badge-success">Text</span>'
        ),
        (
            ((('class', 'badge-success'), ), ),
            '<span class="badge badge-success"></span>'
        ),
        (
            ((('class', 'badge-success'), ('href', '#'), ), ),
            '<a class="badge badge-success" href="#"></a>'
        ),
    ))
    def test_make_badge(self, input, output):
        assert Components.make_badge(*input) == output

    def test_make_alert(self):
        pass

    def test_make_breadcrumb(self):
        pass

    def test_make_button(self):
        pass

    def test_make_button_group(self):
        pass

    def test_make_card(self):
        pass

    def test_make_carousel(self):
        pass

    def test_make_dropdown(self):
        pass

    def test_make_form(self):
        pass

    def test_make_input_group(self):
        pass

    def test_make_jumbotron(self):
        pass

    def test_make_lmaket_group(self):
        pass

    def test_make_modal(self):
        pass

    def test_make_nav(self):
        pass

    def test_make_navbar(self):
        pass

    def test_make_pagination(self):
        pass

    def test_make_popover(self):
        pass

    def test_make_progres(self):
        pass

    def test_make_scrollspy(self):
        pass

    def test_make_tooltip(self):
        pass
