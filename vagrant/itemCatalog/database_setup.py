from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    """
    The User Class i used to store information about our users
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

class Catagory(Base):
    """
    The Catagory Class is used to store information about our high level catagories
    """
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
    """
    The Item class is used to store specific sport items
    """
    __tablename__ = "item"

    id = Column(Integer, primary_key = True)
    title = Column(String(250), nullable = False)
    description = Column(Text, nullable = False)
    date_added = Column(DateTime, nullable = False)
    cat_id = Column(Integer, ForeignKey('catagory.id'))
    catagory = relationship(Catagory)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.title,
            'id': self.id,
            'date_added': self.date_added,
            'description': self.description,
            'user_id': self.user_id,
        }

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
