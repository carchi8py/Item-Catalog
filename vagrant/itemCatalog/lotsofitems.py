import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catagory, Item, Base, User

def add_and_commit(session, item):
    session.add(item)
    session.commit()

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Create teh Admin user
user1 = User(name="Super Admin", email="none@null.com", picture="http://www.practical-programming.org/articles/love_null/images/null-pointer-exception.png")
session.add(user1)
session.commit()
catagory1 = Catagory(name = "Soccer")
add_and_commit(session, catagory1)

item1 = Item(user_id=1, title = "Soccer Cleats", description = "You wear them on your feet", catagory=catagory1, date_added = datetime.datetime.now())
add_and_commit(session, item1)

item2 = Item(user_id=1, title = "Jersey", description = "You wear it on your body", catagory=catagory1, date_added = datetime.datetime.now())
add_and_commit(session, item2)


catagory2 = Catagory(name = "Basketball")
add_and_commit(session, catagory2)

item1 = Item(user_id=1, title = "Basketball", description = "The Ball you play with", catagory=catagory2, date_added = datetime.datetime.now())
add_and_commit(session, item1)

item2 = Item(user_id=1, title = "Basketball Jersey", description = "You wear it on your body", catagory=catagory2, date_added = datetime.datetime.now())
add_and_commit(session, item2)

catagory3 = Catagory(name = "Baseball")
add_and_commit(session, catagory3)

catagory4 = Catagory(name = "Frisbee")
add_and_commit(session, catagory4)

catagory5 = Catagory(name = "Snowboarding")
add_and_commit(session, catagory5)

item1 = Item(user_id=1, title = "Goggles", description = "You put them on your face", catagory=catagory5, date_added = datetime.datetime.now())
add_and_commit(session, item1)

item2 = Item(user_id=1, title = "Snowboard", description = "You step on it and ride down a mountain", catagory=catagory5, date_added = datetime.datetime.now())
add_and_commit(session, item2)

yesterday = datetime.datetime.now() - datetime.timedelta(1)
old_item = Item(user_id=1, title = "Old Snowboard", description = "You step on it and ride down a mountain", catagory=catagory5, date_added = yesterday)
add_and_commit(session, old_item)

catagory6 = Catagory(name = "Rock Climbing")
add_and_commit(session, catagory6)

catagory7 = Catagory(name = "Foosball")
add_and_commit(session, catagory7)

catagory8 = Catagory(name = "Skating")
add_and_commit(session, catagory8)

catagory9 = Catagory(name = "Hockey")
add_and_commit(session, catagory9)
