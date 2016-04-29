from flask import Flask, render_template
app = Flask(__name__)

categories = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

@app.route('/')
@app.route('/catalog/')
def showCatalog():
    return render_template('catalog.html', categories = categories)

@app.route('/catalog/<category>/items')
def showCategory(category):
    return "This page show all %s" % category

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