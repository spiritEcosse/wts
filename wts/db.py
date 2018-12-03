"""Base Model."""
from sqlalchemy.orm import load_only

import pandas as pd
from sqlalchemy_filters import apply_filters


class ModelMixin:
    """Base Model with hooks methods."""

    def __repr__(self):
        """View object class."""
        return "<{}(name='{}')>".format(self.__class__.__name__, self.name)

    def save(self):
        """
        Save object to db.

        Return this object.
        """
        self.query.session.add(self)
        self.query.session.commit()
        return self

    def delete(self):
        """
        Delete object from db.

        Return this object.
        """
        self.query.session.delete(self)
        self.query.session.commit()
        return self

    @classmethod
    def pd_name(cls, filter_spec=None):
        """
        Get names by filter from this class.

        return: list names.
        """

        query = apply_filters(cls.query, filter_spec) \
            if filter_spec else cls.query

        return list(pd.read_sql(
            query.options(load_only("name")).statement,
            cls.query.session.bind
        ).name)
