import pytest
from html_.analyze import Analyze


class TestAnalyze:
    def test_is_alert(self):
        pass

    @pytest.mark.parametrize("input,output", (
        ('<span class="badge badge-primary"></span>', True),
        ('<span class="badge"></span>', True),
        ('<span></span>', False),
        ('<span class="badge-primary"></span>', True),
        ('<a class="badge-primary"></a>', True),
        ('<div class="badge-primary"></div>', False),
        ('<table class="badge-primary"></table>', False),
        ("""
        <h1>Example heading <span class="badge badge-secondary">New</span></h1>
        """, False),
    ))
    def test_is_badge(self, input, output):
        assert Analyze.is_badge(input) == output

    # def test_is_breadcrumb(self):
    #     pass
    #
    # def test_is_button(self):
    #     pass
    #
    # def test_is_button_group(self):
    #     pass
    #
    # def test_is_card(self):
    #     pass
    #
    # def test_is_carousel(self):
    #     pass
    #
    # def test_is_dropdown(self):
    #     pass
    #
    # def test_is_form(self):
    #     pass
    #
    # def test_is_input_group(self):
    #     pass
    #
    # def test_is_jumbotron(self):
    #     pass
    #
    # def test_is_list_group(self):
    #     pass
    #
    # def test_is_modal(self):
    #     pass
    #
    # def test_is_nav(self):
    #     pass
    #
    # def test_is_navbar(self):
    #     pass
    #
    # def test_is_pagination(self):
    #     pass
    #
    # def test_is_popover(self):
    #     pass
    #
    # def test_is_progres(self):
    #     pass
    #
    # def test_is_scrollspy(self):
    #     pass
    #
    # def test_is_tooltip(self):
    #     pass
