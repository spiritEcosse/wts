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
        self.bs_input = Bs(html=bs_input)

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
        self.bs_input.div.add_text_color()
        self.bs_input.div.add_bg()
        self.bs_input.div.add_border()
        self.bs = self.tree(self.bs_input.div)
        return self.prettify()

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
        tag.known_classes()

        tag.add_center() if tag.need_center() else None
        tag.add_icon() if tag.is_icon() else None

        tag.attrs.pop('style') if 'style' in tag.attrs else None

        if tag.display_block() and not bool(tag.attrs.get('class', False)):
            tag.attrs['class'] = ['d-block']

        if parent_tag and tag.need_merge():
            new_tag = parent_tag

            if new_tag.has_class() and tag.has_class():
                new_tag.attrs['class'].extend(tag.attrs['class'])
        else:
            new_tag = self.bs.new_tag(tag.name, **tag.attrs)

        for child in tag.contents:
            if child != '\n':
                if type(child) is NavigableString:
                    new_tag.append(child)

                    if tag.display_block() and new_tag is parent_tag:
                        new_tag.string = 'People'
                        new_tag.string.wrap(
                            self.bs.new_tag(
                                'p', **{'class': ["card-text"]}
                            )
                        )
                else:
                    tag_child = self.tree(child, new_tag)

                    if new_tag is not tag_child:
                        new_tag.append(tag_child)

        return new_tag
