from bs4 import BeautifulSoup

import pytest
from html_.components import Components


class TestComponenets:
    @pytest.mark.parametrize("input,output", (
        ("""
        card
          card-header
            nav-tabs class "card-header-tabs"
              nav-item
                nav-link class "active" str "Link" attrs "href: #"
              nav-item
                nav-link str "Link" attrs "href: #"
              nav-item
                nav-link str "Link" attrs "href: #"
              nav-item
                nav-link class "disabled" str "Link" attrs "href: #"
        """, BeautifulSoup()),
        ("""
        card
          card-header str "Content"
          card-body
            blockquote
              p str "Content"
              blockquote-footer str "Content" class mb-0
                cite str "Content" title "Title"
        """,
         BeautifulSoup(, "html.parser")
         ),
    ))
    def test_make_component(self, input, output):
        assert Components.make_componenet(input) == output.prettify()
