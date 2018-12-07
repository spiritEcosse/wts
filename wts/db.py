"""Base Model."""

from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import load_only, object_mapper, properties

import pandas as pd
from sqlalchemy_filters import apply_filters


class ModelMixin:
    """Base Model with hooks methods."""

    def __repr__(self):
        """View object class."""
        return "<{}(name='{}')>".format(self.__class__.__name__, self.name)

    def to_dict(self, fields=[]):
        return {
            field: getattr(self, field) for field in fields or self.columns()
        }

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

            for field in self.columns():
                value = getattr(self, field, None)

                if value is not None:  # field maybe is None
                    setattr(find, field, value)

            self = find
            commit()

        return self

    def columns(self):
        """Returns all fields for this model excluding id and including
        fields of related models.

        Parameters
        ----------


        Returns
        -------
        type: list
            Returns list of str.

        """
        columns = inspect(self).attrs.keys()
        columns.remove('id')
        return columns

    def rel(self, rel_prop, iterable):
        """Creates objects of related models without creating them in the
        database.

        Parameters
        ----------
        rel_prop : type sqlalchemy.orm.properties.RelationshipProperty
            Object RelationshipProperty.
        iterable : type list.
            List with nested dictionaries.

        Returns
        -------
        type : list
            Returns list objects of related models.

        """
        return list(map(
            lambda data: rel_prop.mapper.class_(**data), iterable
        ))

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

    @classmethod
    def group_by(cls, field='name'):
        return cls.query.group_by(field).all()

    def relf(self):
        """Get a list of fields that have connections to other models.

        Parameters
        ----------


        Returns
        -------
        type: list
            List of objects of type
            sqlalchemy.orm.properties.RelationshipProperty.

        """
        return list(filter(
            lambda p: isinstance(p, properties.RelationshipProperty),
            object_mapper(self).iterate_properties
        ))
