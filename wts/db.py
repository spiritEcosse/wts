"""Base Model."""

from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
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
        Auto update if caught IntexgrityError.

        Parameters
        ----------


        Returns
        -------
        type
            The object of the model that inherits this mixin.

        """

        def commit():
            self.query.session.add(self)
            self.query.session.commit()

        try:
            commit()
        except IntegrityError:
            self.query.session.rollback()
            self.query.session.flush()

            find = self.query.filter_by(name=self.name).one()
            columns = inspect(self).attrs.keys()
            columns.remove('id')

            for field in columns:
                value = getattr(self, field, None)

                if value is not None:  # field maybe is None
                    setattr(find, field, value)

            self = find
            commit()

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

        query = cls.filter(filter_spec) if filter_spec else cls.query

        return list(pd.read_sql(
            query.options(load_only("name")).statement,
            cls.query.session.bind
        ).name)

    @classmethod
    def filter(cls, filter_spec):
        return apply_filters(cls.query, filter_spec)
