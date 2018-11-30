"""Analyze html structure."""

from bs4 import BeautifulSoup

from wts import settings


class Analyze(object):
    """Analyze html structure."""

    def __init__(self, css={}, html=''):
        """Init ."""
        self.css = css
        self.html = html

    def append(self):
        """
        Check the visual following content.

        Whether this object can add other objects.
        """
        if self.value.inline and self.value.block:
            return self.check_width()

        if self.value.block or self.value.inline:
            if hasattr(self, 'float'):
                return self.float == 'left' and self.check_width()

        return self.value.inline

    def check_width(self):
        return getattr(self, 'width', settings.WINDOWS_WIDTH) <= \
            settings.WINDOWS_WIDTH

    def horizontal_center(self):
        return (getattr(self, 'display', '') == 'flex'
                and getattr(self, 'justify-content', '') == 'center') or \
            (getattr(self, 'display', None) in
             ['block', 'inline', 'inline-block']
             and getattr(self, 'text-align', '') == 'center')

    def vertical_center(self):
        return self.css.get('align-self', '') == 'center' \
            or self.css.get('align-items', '') == 'center'

    def merge(self):
        if self.css:
            return self.css.get('width') == self.css.get('parent_width')
        return len(BeautifulSoup(self.html, "html.parser").find_all()) == 2
