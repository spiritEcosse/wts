from bs4.element import NavigableString

from apps.bs import Bs
from apps.html.analyze import Analyze


class Builder():
    classes = {"card", "card-img-top",
               "card-body", "card-title", "card-text", "bg-primary",
               "border-none", "p-4", "text-center", "text-white", "row",
               "d-flex", "col-5", "align-self-center", "container",
               "justify-content-center"}

    def __init__(self, bs_input):
        self.bs = Bs()
        self.bs_input = Bs(bs_input)

    def prettify(self):
        return self.bs.prettify()

    def run(self):
        self.bs = self.tree(self.bs_input.div)
        # self.bs.contents[0].attrs['class'].extend([
        #     self.add_color_text(), self.add_bg(), self.add_border()
        # ])

    def tree(self, soup, parent_tag=''):
        # if 'class' in soup.attrs:
        #     self.attrs_class(soup)

        if parent_tag and soup.need_merge:
            tag = parent_tag
            tag.attrs['class'].extend(soup.attrs['class'])
        else:
            tag = self.bs.new_tag(soup.name, **soup.attrs)

        for child in soup.contents:
            if child != '\n':
                if type(child) is NavigableString:
                    tag.append(child)
                else:
                    tag_child = self.tree(child, tag)

                    if tag is not tag_child:
                        tag.append(tag_child)

        return tag

    def attrs_class(self, soup):
        self.add_class(soup)
        self.clear_class(soup)

    def clear_class(self, soup):
        soup.attrs['class'] = set(soup.attrs['class'])
        soup.attrs['class'].intersection_update(self.classes)
        soup.attrs['class'] = list(soup.attrs['class'])

    def add_color_text(self):
        return 'text-white'

    def add_bg(self):
        return 'bg-primary'

    def add_border(self):
        return 'border-none'

    def add_align_self_center(self):
        return 'align-self-center'

    def horizontal_center(self):
        return 'text-center'

    def add_class(self, soup):
        # css = self.get_css_styles()
        css = {}
        analyze = Analyze()

        if analyze.horizontal_center():
            soup.attrs['class'].append(self.horizontal_center())

        if analyze.vertical_center():
            soup.attrs['class'].append(self.add_align_self_center())

        # check_bg
        # check_color
        # check_border
