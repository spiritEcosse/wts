from bs4 import BeautifulSoup
from sqlalchemy import and_

from apps.html.models import Classes
from selenium import webdriver
from wts import settings


class Bs(BeautifulSoup):
    def __init__(self, url='', features="html.parser", **kwargs):
        html = ''

        if url:
            driver = webdriver.Remote(
                command_executor=settings.REMOTE_DRIVER,
                desired_capabilities=settings.CAPABILITIES,
            )
            driver.get(url)
            self.__class__.__base__.__base__.driver = driver
            html = driver.page_source

        return super().__init__(html, features, **kwargs)


class Tag():
    @property
    def xpath(self):
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
    def width(self):
        element = self.driver.find_element_by_xpath(self.xpath)
        return element.value_of_css_property('width')

    @property
    def need_merge(self):
        classes = Classes.query.filter(and_(
            Classes.name.in_(self.attrs['class']),
            Classes.belong_to_component == True
        )).scalar() is None

        return classes and self.width == self.parent.width
        # return len(BeautifulSoup(self.html, "html.parser").find_all()) == 2


for prop_name in dir(Tag):  # noqa
    prop = getattr(Tag, prop_name)

    if isinstance(prop, property):
        setattr(Bs.__base__.__base__, prop_name, prop)

# styles = driver.execute_script(
#     'var items = {};'
#     + 'var compsty = getComputedStyle(arguments[0]);'
#     + 'var len = compsty.length;'
#     + 'for (index = 0; index < len; index++)'
#     + '{items [compsty[index]] = compsty.getPropertyValue(compsty[index])};'
#     + 'return items;', element)
