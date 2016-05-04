from flask import Flask, render_template
app = Flask(__name__)

catagory = {'name': 'The CRUDdy Crab', 'id': '1'}
categories = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.route('/')
@app.route('/catalog/')
def showCatalog():
    return render_template('main.html', categories = categories)

@app.route('/catalog/<category>/items')
def showCategory(category):
    return render_template('category.html', categories = categories, catagory = catagory, items = items)    

@app.route('/catalog/<category>/<item>')
def showItems(category, item):
    return "This is a %s from %s" % (item, category)

@app.route('/catalog/<item>/edit')
def editItem(item):
    return "This page allows the user to edit %s" % item

@app.route('/catalog/<item>/delete')
def deleteItem(item):
    return "This page allows the user to delete %s" % item

if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0", port = 8000)