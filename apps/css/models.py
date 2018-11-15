"""Models to describe the tables of css app."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

Base = declarative_base()


class Property(Base):
    """
    Css layout.

    Css properties.
    """

    __tablename__ = 'property'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    values = relationship("Value", backref="property")

    def __repr__(self):
        """View object class."""
        return "<{}(name='{}')>".format(self.__class__.__name__, self.name)


class Value(Base):
    """
    Css layout.

    Css values.
    """

    __tablename__ = 'value'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    property_id = Column(
        Integer,
        ForeignKey('property.id', onupdate="CASCADE", ondelete="CASCADE")
    )
    property = relationship("Property")

    def __repr__(self):
        """View object class."""
        return "<{}(name='{}')>".format(self.__class__.__name__, self.name)
