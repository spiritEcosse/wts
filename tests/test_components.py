from bs4 import BeautifulSoup

import pytest
from html_.components import Components


class TestComponenets:
    def test_make_alert(self):
        pass

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

    @pytest.mark.parametrize("input,output", (
        ((), BeautifulSoup("""
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item active" aria-current="page">
                    </li>
                </ol>
            </nav>""", "html.parser")
         ),
        ((('Home', 'Library', ), ), BeautifulSoup("""
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="#">Home</a></li>
                    <li class="breadcrumb-item active" aria-current="page">
                        Library
                    </li>
                </ol>
            </nav>""", "html.parser")
         ),
        ((('Home', 'Library', 'Data', ), ), BeautifulSoup("""
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="#">Home</a></li>
                    <li class="breadcrumb-item">
                        <a href="#">Library</a>
                    </li>
                    <li class="breadcrumb-item active" aria-current="page">
                        Data
                    </li>
                </ol>
            </nav>""", "html.parser")
         ),
    ))
    def test_make_breadcrumb(self, input, output):
        assert Components.make_breadcrumb(*input) == output.prettify()

    # def test_make_button(self):
    #     pass
    #
    # def test_make_button_group(self):
    #     pass
    #
    # def test_make_card(self):
    #     pass
    #
    # def test_make_carousel(self):
    #     pass
    #
    # def test_make_dropdown(self):
    #     pass
    #
    # def test_make_form(self):
    #     pass
    #
    # def test_make_input_group(self):
    #     pass
    #
    # def test_make_jumbotron(self):
    #     pass
    #
    # def test_make_lmaket_group(self):
    #     pass
    #
    # def test_make_modal(self):
    #     pass
    #
    # def test_make_nav(self):
    #     pass
    #
    # def test_make_navbar(self):
    #     pass
    #
    # def test_make_pagination(self):
    #     pass
    #
    # def test_make_popover(self):
    #     pass
    #
    # def test_make_progres(self):
    #     pass
    #
    # def test_make_scrollspy(self):
    #     pass
    #
    # def test_make_tooltip(self):
    #     pass
