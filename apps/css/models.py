"""Models to describe the tables of css app."""

from sqlalchemy.orm import load_only
from sqlalchemy.sql import expression

import pandas as pd
from app import db
from wts.db import ModelMixin


class Property(ModelMixin, db.Model):
    """
    Css layout.

    Css properties.
    """

    __tablename__ = 'property'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)


class Value(ModelMixin, db.Model):
    """
    Css layout.

    Css values.
    """

    __tablename__ = 'value'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    property_id = db.Column(
        db.Integer,
        db.ForeignKey('property.id', onupdate="CASCADE", ondelete="CASCADE")
    )
    property = db.relationship(
        "Property", backref=db.backref('values', lazy=True)
    )
    inline = db.Column(
        db.Boolean, server_default=expression.true(), nullable=False
    )
    block = db.Column(
        db.Boolean, server_default=expression.true(), nullable=False
    )
    __table_args__ = (
        db.UniqueConstraint(
            'property_id', 'name', name='_name__property_id__uc'),
    )

    @classmethod
    def pd_name_by_pr(cls, pr):
        """Get all names from this class by property."""
        pr = Property.query.filter_by(name='display').one()

        return pd.read_sql(
            cls.query.with_parent(pr).options(load_only("name")).statement,
            db.session.bind
        ).name
