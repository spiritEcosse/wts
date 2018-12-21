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


class Tag:
    def __init__(self, parser=None, builder=None, name=None, namespace=None,
                 prefix=None, attrs=None, parent=None, previous=None,
                 is_xml=None):
        "Basic constructor."
        self.driver = getattr(parser, 'driver', None)

        if parser is None:
            self.parser_class = None
        else:
            # We don't actually store the parser object: that lets extracted
            # chunks be garbage-collected.
            self.parser_class = parser.__class__
        if name is None:
            raise ValueError("No value provided for new tag's name.")
        self.name = name
        self.namespace = namespace
        self.prefix = prefix
        if builder is not None:
            preserve_whitespace_tags = builder.preserve_whitespace_tags
        else:
            if is_xml:
                preserve_whitespace_tags = []
            else:
                preserve_whitespace_tags = HTMLAwareEntitySubstitution.preserve_whitespace_tags
        self.preserve_whitespace_tags = preserve_whitespace_tags
        if attrs is None:
            attrs = {}
        elif attrs:
            if builder is not None and builder.cdata_list_attributes:
                attrs = builder._replace_cdata_list_attribute_values(
                    self.name, attrs)
            else:
                attrs = dict(attrs)
        else:
            attrs = dict(attrs)

        # If possible, determine ahead of time whether this tag is an
        # XML tag.
        if builder:
            self.known_xml = builder.is_xml
        else:
            self.known_xml = is_xml
        self.attrs = attrs
        self.contents = []
        self.setup(parent, previous)
        self.hidden = False

        # Set up any substitutions, such as the charset in a META tag.
        if builder is not None:
            builder.set_up_substitutions(self)
            self.can_be_empty_element = builder.can_be_empty_element(name)
        else:
            self.can_be_empty_element = False

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
        return self._value_of_css_property('width')

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

    # @property
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
        check = [self.width() == self.parent.width()]

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

    def clear_class(self):
        if self.has_class():
            filter_spec = [
                {'field': 'name', 'op': 'in', 'value': self.attrs['class']},
            ]
            self.attrs['class'] = Classes.pd_name(filter_spec)


for prop_name in dir(Tag):  # noqa
    prop = getattr(Tag, prop_name)

    if isinstance(prop, property) or type(prop) is FunctionType:
        setattr(Bs.__base__.__base__, prop_name, prop)

# styles = driver.execute_script(
#     'var items = {};'
#     + 'var compsty = getComputedStyle(arguments[0]);'
#     + 'var len = compsty.length;'
#     + 'for (index = 0; index < len; index++)'
#     + '{items [compsty[index]] = compsty.getPropertyValue(compsty[index])};'
#     + 'return items;', element)
