from bs4.element import NavigableString

from apps.bs.base import Bs
from apps.html.analyze import Analyze


class Builder():
    def __init__(self, bs_input):
        """Object initialization.

        Parameters
        ----------
        bs_input : str
            This parameter will be passed for the class BeautifulSoup,
            for the basis of the layout. `bs_input`.

        Returns
        -------
        None

        """
        self.bs = Bs()
        self.bs_input = Bs(bs_input)

    def prettify(self):
        """
        Make readable layout presentation from 'bs'.

        Parameters
        ----------

        Returns
        -------
        type: str
            Readable layout presentation.

        """
        return self.bs.prettify()

    def run(self):
        """
        The method responsible for running the recursive creation of html
        structure, based on `bs_input`.

        Writing result to attribute bs.
        Parameters
        ----------

        Returns
        -------
        type: None

        """
        self.bs_input.div.add_bg()
        self.bs_input.div.add_border()
        self.bs = self.tree(self.bs_input.div)

    def tree(self, tag, parent_tag=''):
        """The main method passes through all elements of the tree recursively.

        Parameters
        ----------
        tag : bs4.element.Tag
            Html tag.
        parent_tag : bs4.element.Tag
            Parent html tag for tag `tag`.
            Default - ''.

        Returns
        -------
        type : bs4.element.Tag
            Creates a new html tag `new_tag` based on attributes and type
            `tag`.

        """
        tag.clear_class()

        if parent_tag and tag.need_merge:
            new_tag = parent_tag
            new_tag.attrs['class'].extend(tag.attrs['class'])
        else:
            new_tag = self.bs.new_tag(tag.name, **tag.attrs)

        for child in tag.contents:
            if child != '\n':
                if type(child) is NavigableString:
                    new_tag.append(child)
                else:
                    tag_child = self.tree(child, new_tag)

                    if new_tag is not tag_child:
                        new_tag.append(tag_child)

        return new_tag

    def add_class(self, soup):
        # css = self.get_css_styles()
        analyze = Analyze()

        if analyze.horizontal_center():
            soup.attrs['class'].append(self.horizontal_center())

        if analyze.vertical_center():
            soup.attrs['class'].append(self.add_align_self_center())
