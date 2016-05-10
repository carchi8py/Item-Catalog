from flask import Flask, render_template
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Catagory, Item, Base


app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



#catagory = {'name': 'The CRUDdy Crab', 'id': '1'}
#categories = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
#item1 =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

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

@app.route('/catalog/<item>/edit')
def editItem(item):
    categories = session.query(Catagory)
    item = session.query(Item).filter_by(title = item).one()
    return render_template('editItem.html', item = item, categories = categories)

@app.route('/catalog/<item>/delete')
def deleteItem(item):
    return render_template('deleteItem.html', item = item1)

@app.route('/catalog/item/new')
def newItem():
    return render_template('newItem.html', categories = categories)

if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0", port = 8000)