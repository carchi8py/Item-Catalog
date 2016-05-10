import datetime

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Catagory, Item, Base

app = Flask(__name__)

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
        print 'hi'
        print request.form['catagories']
        category = session.query(Catagory).filter_by(name = request.form['catagories']).one()
        print '1'
        print request.form['title']
        print request.form['description']
        newItem = Item(title = request.form['title'], description=request.form['description'], catagory=category, date_added = datetime.datetime.now())
        print '2'
        session.add(newItem)
        print '3'
        session.commit()
        print '4'
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newItem.html', categories = categories)

if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0", port = 8000)