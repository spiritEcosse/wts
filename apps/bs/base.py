import re
import uuid
from types import FunctionType

from bs4 import BeautifulSoup
from bs4.element import Tag as BaseTag

from apps.html.models import Classes
from sqlalchemy_filters import apply_filters
from wts.settings import FILE_HTML, URL_FILE_HTML
from wts.utils import create_driver


class Bs(BeautifulSoup):
    def __init__(self, url='', html='', features="html.parser", **kwargs):
        self.html = ""

        if html:
            path = FILE_HTML.format(str(uuid.uuid4()))
            with open(path, "w") as f:
                f.write(html)
                url = URL_FILE_HTML.format(path)

        if url:
            self.driver = create_driver()
            self.driver.get(url)
            self.html = self.driver.page_source

        super().__init__(self.html, features, **kwargs)


class Tag(BaseTag):
    def __init__(self, *args, prop={}, we_known_classes=set(), **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = getattr(self.parser, 'driver', None)
        [setattr(self, key, val) for key, val in prop.items()]
        self.we_known_classes = we_known_classes

    def _value_of_css_property(self, property):
        """Return css property value via selenium.

        Parameters
        ----------
        property : str
            The name of one of the key properties of css styles.

        Returns
        -------
        type: str
            Unformatted string.

        """
        element = self.driver.find_element_by_xpath(self.xpath())
        return element.value_of_css_property(property)

    @property
    def width(self):
        """Return css property value width for this tag via selenium.
        Parameters
        ----------

        Returns
        -------
        type: str
            Unformatted string.

        """
        return int(self._width or 0)

    @width.setter
    def width(self, value=None):
        self._width = value or self._value_of_css_property('width')

    def xpath(self):
        """Makes up the 'xpath' of the parents of this object.

        Parameters
        ----------

        Returns
        -------
        type: str
            Returns a string of the form '/html/body/div'.

        """
        components = []
        child = self if self.name else self.parent

        for parent in child.parents:
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name
                if siblings == [child] else
                '%s[%d]' % (child.name, 1 + siblings.index(child))
            )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)

    @property
    def bgc(self):
        """Return css property value background-color for this tag via
        selenium.

        Parameters
        ----------

        Returns
        -------
        type: str
            Unformatted string.

        """
        return self._value_of_css_property('background-color')

    def border(self):
        """Return css property value border for this tag via
        selenium.

        Parameters
        ----------

        Returns
        -------
        type: tuple
            Tuple format - (size, style, color, ).

        """
        match = re.match(
            r"(\d+)px (\w+) (.*)",
            self._value_of_css_property('border')
        )
        return match.group(1, 2, 3)

    def add_bg(self):
        if self.bgc != 'rgba(0, 0, 0, 0)':
            self.attrs['class'].append('bg-primary')

    def add_border(self):
        if self.has_class():
            if Classes.have_pr(self.attrs['class'], 'border') is not None:
                if not int(self.border()[0]):
                    self.attrs['class'].append('border-none')

    def need_merge(self):
        """Checks whether you need to add the child to the parent.

        Parameters
        ----------

        Returns
        -------
        type: bool
            Returns true if it is necessary to combine both classes otherwise
            False.

        """
        check = [self.width == self.parent.width]

        if self.has_class():
            filter_spec = [
                {
                    'and': [
                        {'field': 'name', 'op': 'in',
                            'value': self.attrs['class']},
                        {'field': 'belong_to_component',
                            'op': '==', 'value': True},
                    ]
                }
            ]
            check.append(
                apply_filters(Classes.query, filter_spec).scalar() is None
            )

        return all(check)

    def has_class(self):
        """Check only class.

        Parameters
        ----------

        Returns
        -------
        type: bool
            Returns true if the class is in attrs, otherwise False.

        """
        return self.has_attr('class')

    def known_classes(self):
        """Returns the cleared list of classes, based on known to us.

        Parameters
        ----------


        Returns
        -------
        type: list
            List of str.

        """
        res = []

        if self.we_known_classes:
            res = list(
                set(self.attrs['class']).intersection(self.we_known_classes)
            )
        else:
            filter_spec = [
                {'field': 'name', 'op': 'in', 'value': self.attrs['class']},
            ]
            res = Classes.pd_name(filter_spec)

        return res


# styles = driver.execute_script(
#     'var items = {};'
#     + 'var compsty = getComputedStyle(arguments[0]);'
#     + 'var len = compsty.length;'
#     + 'for (index = 0; index < len; index++)'
#     + '{items [compsty[index]] = compsty.getPropertyValue(compsty[index])};'
#     + 'return items;', element)
