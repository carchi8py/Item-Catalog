import datetime
import random
import string

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Catagory, Item, Base, User

app = Flask(__name__)

#Steps to create Flash login session
from flask import session as login_session

#Imports for Oauth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog/')
def showCatalog():
    """
    The Main page of our website
    """
    categories = session.query(Catagory)
    latest_items = session.query(Item).order_by(Item.date_added.desc())
    #If the user is logged in we want to show their picture in the status bar of the website
    if 'username' not in login_session:
        return render_template('pubMain.html', categories = categories, items = latest_items)
    else:
        return render_template('main.html', categories = categories, items = latest_items, image=login_session['picture'])

@app.route('/catalog.json')
def showCatalogJSON():
    """
    The json version of our main page
    """
    categories = session.query(Catagory)
    return jsonify(Catagorys=[i.serialize for i in categories])

@app.route('/catalog/<category>/items')
def showCategory(category):
    """
    Show a specific sport catagory
    """
    categories = session.query(Catagory)
    category = session.query(Catagory).filter_by(name = category).one()
    items = session.query(Item).filter(Item.cat_id == category.id)
    #If the user is logged in we want to show their picture in the status bar of the website
    if 'username' not in login_session:
        return render_template('category.html', categories = categories, catagory = category, items = items, image=None)
    else:
        return render_template('category.html', categories = categories, catagory = category, items = items, image=login_session['picture'])

@app.route('/catalog/<category>/items.json')
def showCategoryJSON(category):
    """
    The json version of our Items
    """
    categories = session.query(Catagory)
    category = session.query(Catagory).filter_by(name = category).one()
    items = session.query(Item).filter(Item.cat_id == category.id)
    return jsonify(Items=[i.serialize for i in items])

@app.route('/catalog/<category>/<item>')
def showItems(category, item):
    """
    Shows a specific item in the database
    """
    category = session.query(Catagory).filter_by(name = category).one()
    item = session.query(Item).filter(Item.cat_id == category.id).filter_by(title = item).one()
    creator = getUserInfo(item.user_id)
    #if the user is not logged in return the public page
    if 'username' not in login_session:
        return render_template('pubItem.html', item = item, image=None)
    #if the user is logged in dosn't own the item, show the public page, but show their picture
    elif creator.id != login_session['user_id']:
        return render_template('pubItem.html', item = item, image=login_session['picture'])
    #if the user is logged in and owns the item, show them the page they can modify it
    else:
        return render_template('item.html', item = item, image=login_session['picture'])

@app.route('/catalog/<item>/edit', methods=['GET', 'POST'])
def editItem(item):
    """
    Allows a user to edit an item from the database
    """
    #if the user isn't logged, they shouldn't see this page
    if 'username' not in login_session:
        return redirect('/login')
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
        return render_template('editItem.html', item = item, categories = categories, image=login_session['picture'])

@app.route('/catalog/<item>/delete', methods=['GET', 'POST'])
def deleteItem(item):
    """
    Allow a user to delete an item
    """
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(title = item).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteItem.html', item = item, image=login_session['picture'])

@app.route('/catalog/item/new', methods=['GET', 'POST'])
def newItem():
    """
    Allow the user to create a new item
    """
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Catagory)
    if request.method == 'POST':
        category = session.query(Catagory).filter_by(name = request.form['catagories']).one()
        newItem = Item(title = request.form['title'], description=request.form['description'], catagory=category, date_added = datetime.datetime.now(), user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newItem.html', categories = categories, image=login_session['picture'])


### ALL LOGIN Functions ###


@app.route('/login')
def showLogin():
    """
    Show the login page for the user
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Checks with google if the user is authenticated or not
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

@app.route('/gdisconnect')
def gdisconnect():
    """
    Sign Google user out of the site
    """
    access_token = login_session['access_token']
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
    
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

### HELPER FUNCTIONS ###


def createUser(login_session):
    """
    Create a new user in the database
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    """
    Get the user object from a user id
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """
    Get the user object from a user email
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == '__main__':
    #lol
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = "0.0.0.0", port = 8000)