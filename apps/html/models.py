"""Models to describe the tables of db."""

from sqlalchemy.sql import expression

from app import db
from wts.db import ModelMixin


class Classes(ModelMixin, db.Model):
    """
    Classes for tags.

    Model hold list from attr class tag.
    <div class="class1"></div>
        (class1, )
    <div class="class1 class2"></div>
        (class1, class2, )
    """

    __tablename__ = 'class'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
    belong_to_component = db.Column(
        db.Boolean, server_default=expression.true(), nullable=False
    )

# Base = declarative_base()
#
#
# tags_components = Table(
#     'tags_components', Base.metadata,
#     Column('tag_id', ForeignKey('tags.id'), primary_key=True),
#     Column('component_id', ForeignKey('components.id'), primary_key=True)
# )
#
# components_childrens = Table(
#     'components_childrens', Base.metadata,
#     Column('component_id', Integer, ForeignKey('components.id'),
#            primary_key=True),
#     Column('children_id', Integer, ForeignKey('components.id'),
#            primary_key=True)
# )
#
# # utilities_components = Table(
# #     'utilities_components', Base.metadata,
# #     Column('utility_id', ForeignKey('utilities.id'), primary_key=True),
# #     Column('component_id', ForeignKey('components.id'), primary_key=True)
# # )
#
#
# class Tag(Base):
#     """
#     Tags.
#
#     Model to describe the tags of html.
#     """
#
#     __tablename__ = 'tags'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True)
#     closing = Column(Boolean, server_default=True)
#     components = relationship(
#         'Component', secondary=tags_components, back_populates='tags'
#     )
#
#     def __repr__(self):
#         """View object class."""
#         return "<{}(name='{}')>".format(self.__class__.__name__, self.name)
#
#
# class Component(Base):
#     """
#     Html structure.
#
#     Model to describe the componenets of html.
#     """
#
#     __tablename__ = 'components'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True)
#     tag = Column(ForeignKey('tags.id'))
#     # tags = relationship(
#     #     'Tag', secondary=tags_components, back_populates='components'
#     # )
#     attrs = Column(ARRAY(String))
#     # utilities = relationship(
#     #     "Utility", secondary=utilities_components,
#     #     back_populates='components'
#     # )
#     # childrens = relationship(
#     #     "Component", secondary=components_childrens,
#     #     primaryjoin=id == components_childrens.c.component_id,
#     #     secondaryjoin=id == components_childrens.c.children_id,
#     # )
#
#     def __repr__(self):
#         """View object class."""
#         return "<{}(name='{}')>".format(self.__class__.__name__, self.name)
#
#
# # class Utility(Base):
# #     """
# #     Extra classes for tags.
# #
# #     Model to describe the utilities of html.
# #     """
# #
# #     __tablename__ = 'utilities'
# #
# #     id = Column(Integer, primary_key=True)
# #     name = Column(String)
# #     classes = Column(ARRAY(String))
# #     components = relationship(
# #         'Component', secondary=utilities_components,
#     # back_populates='utilities'
# #     )
# #
# #     def __repr__(self):
# #         """View object class."""
# #         return "<{}(name='{}')>".format(self.__class__.__name__, self.name)
