from sqlalchemy import ARRAY, Boolean, Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

Base = declarative_base()

tags_components = Table('tags_components', Base.metadata,
                        Column('tag_id', ForeignKey(
                            'tags.id'), primary_key=True),
                        Column('component_id', ForeignKey(
                            'components.id'), primary_key=True)
                        )


component_tree = Table(
    'component_tree', Base.metadata,
    Column('component_p_id', Integer, ForeignKey('components.id'),
           primary_key=True),
    Column('component_c_id', Integer, ForeignKey('components.id'),
           primary_key=True)
)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    closing = Column(Boolean, server_default=True)
    components = relationship('Component',
                              secondary=tags_components,
                              back_populates='tags')

    def __repr__(self):
        return "<{}(name='{}')>".format(self.__class__.__name__, self.name)


class Component(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tags = relationship(
        'Tag', secondary=tags_components, back_populates='components')
    classes = Column(ARRAY(String))
    extra_classes = Column(ARRAY(String))
    single = Column(Boolean, server_default=True)
    childrens = Column(Integer, ForeignKey('components.id'))
    friends = relationship("Component", secondary=component_tree,
                           primaryjoin=id == component_tree.c.component_p_id,
                           secondaryjoin=id == component_tree.c.component_c_id,
                           )

    def __repr__(self):
        return "<{}(name='{}')>".format(self.__class__.__name__, self.name)
