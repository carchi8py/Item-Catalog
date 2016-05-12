from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Catagory(Base):
    __tablename__ = "catagory"

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key = True)
    title = Column(String(250), nullable = False)
    description = Column(Text, nullable = False)
    date_added = Column(DateTime, nullable = False)
    cat_id = Column(Integer, ForeignKey('catagory.id'))
    catagory = relationship(Catagory)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.name,
            'id': self.id,
            'date_added': self.date_added,
            'description': self.description,
        }

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
