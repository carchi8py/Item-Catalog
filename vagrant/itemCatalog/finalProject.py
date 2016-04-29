from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/catalog/')
def showCatalog():
    return "This page show all Catalogs"

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