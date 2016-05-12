import datetime
import random
import string

from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Catagory, Item, Base

app = Flask(__name__)

#Steps to create Flash login session
from flask import session as login_session

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Catagory)
    latest_items = session.query(Item).order_by(Item.date_added.desc())
    return render_template('main.html', categories = categories, items = latest_items)

@app.route('/catalog.json')
def showCatalogJSON():
    #TODO figure out how to show items later
    categories = session.query(Catagory)
    return jsonify(Catagorys=[i.serialize for i in categories])

@app.route('/catalog/<category>/items')
def showCategory(category):
    categories = session.query(Catagory)
    category = session.query(Catagory).filter_by(name = category).one()
    items = session.query(Item).filter(Item.cat_id == category.id)
    return render_template('category.html', categories = categories, catagory = category, items = items)    

@app.route('/catalog/<category>/<item>')
def showItems(category, item):
    category = session.query(Catagory).filter_by(name = category).one()
    item = session.query(Item).filter(Item.cat_id == category.id).filter_by(title = item).one()
    return render_template('item.html', item = item)

@app.route('/catalog/<item>/edit', methods=['GET', 'POST'])
def editItem(item):
    categories = session.query(Catagory)
    item = session.query(Item).filter_by(title = item).one()
    if request.method == 'POST':
        if request.form['title']:
            item.title = request.form['title']
        if request.form['description']:
            item.description = request.form['description']
        session.add(item)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('editItem.html', item = item, categories = categories)

@app.route('/catalog/<item>/delete', methods=['GET', 'POST'])
def deleteItem(item):
    item = session.query(Item).filter_by(title = item).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteItem.html', item = item)

@app.route('/catalog/item/new', methods=['GET', 'POST'])
def newItem():
    categories = session.query(Catagory)
    if request.method == 'POST':
        category = session.query(Catagory).filter_by(name = request.form['catagories']).one()
        newItem = Item(title = request.form['title'], description=request.form['description'], catagory=category, date_added = datetime.datetime.now())
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newItem.html', categories = categories)


### ALL LOGIN Functions ###
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    print state
    login_session['state'] = state
    print login_session
    return "The current session state is %s" % login_session['state']

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = "0.0.0.0", port = 8000)