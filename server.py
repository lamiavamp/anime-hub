from flask import Flask, render_template, request
from flask import redirect, url_for, flash, make_response, jsonify
from flask import send_from_directory
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Anime
import random
import string
import requests
import httplib2
import json
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from flask import session as login_session

app = Flask(__name__)

engine = create_engine('sqlite:///anime.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']
APPLICATION_NAME = 'Anime Hub'


# JSON endpoints

@app.route('/categories/<int:category_id>/animes/JSON')
def animesJSON(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    animes = session.query(Anime).filter_by(catg_id=category_id).all()
    return jsonify(Anime=[i.serialize for i in animes])


@app.route('/categories/JSON')
def categoriesJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catgs = session.query(Category).all()
    return jsonify(Category=[i.serialize for i in catgs])


@app.route('/')
@app.route('/index')
def index():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    allanime = getAllAnime()

    topanime = []
    randnums = random.sample(range(1, len(allanime)-1), 3)
    for rand in randnums:
        topanime.append(allanime[rand])

    if 'username' in login_session:
        return render_template('index.html', categories=categories,
                               allanime=allanime[:5], topanime=topanime,
                               username=login_session['username'])

    return render_template('index.html', categories=categories,
                           allanime=allanime[:5], topanime=topanime)


@app.route('/login')
def showLogin():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    username = ""
    if 'username' in login_session:
        return render_template('login.html', STATE=state,
                               username=login_session['username'])
    else:
        return render_template('login.html', STATE=state)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html', username=login_session['username'])


@app.route('/gconnect', methods=['POST'])
def gconnect():
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
        return response

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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
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
    print data

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        print "creating a new user for "+data['email']
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    print "done!"
    return render_template('welcome.html', username=login_session['username'])


# User Helper Functions
def createUser(login_session):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserEmail(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user.email


def getUserID(email):
    try:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        user = session.query(User).filter_by(email=email).one()
        print user.id
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    print h.request
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        print response
        return redirect(url_for('showLogin'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        print response
        return redirect(url_for('showLogin'))


@app.route('/category/<int:catg_id>/')
def showCatg(catg_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    catg = session.query(Category).filter_by(id=catg_id).one()
    animelist = session.query(Anime).filter_by(catg_id=catg_id).all()
    categories = session.query(Category).all()
    if 'username' in login_session:
        return render_template('category.html', animelist=animelist,
                               catg=catg, categories=categories,
                               username=login_session['username'])

    return render_template('category.html', animelist=animelist,
                           catg=catg, categories=categories)


@app.route('/add-anime', methods=['GET', 'POST'])
def addAnime():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()

    if request.method == 'POST':
        newAnime = Anime(title=request.form['title'],
                         description=request.form['desc'],
                         catg_id=request.form['catg'],
                         user_id=(login_session['user_id']))
        session.add(newAnime)
        session.commit()

        print newAnime.id
        print newAnime.user_id

        flash(newAnime.title+" has been successfully added to the list!")
    if 'username' in login_session:
        print login_session['email']
        return render_template('add.html', categories=categories,
                               username=login_session['username'])
    else:
        return render_template('403.html', categories=categories)


@app.route('/category/<int:catg_id>/anime/<int:anime_id>',
           methods=['GET', 'POST'])
def animeDetails(anime_id, catg_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    anime = session.query(Anime).filter_by(id=anime_id).one()
    catg = session.query(Category).filter_by(id=anime.catg_id).one()
    categories = session.query(Category).all()

    if 'username' in login_session:
        if login_session['user_id'] == anime.user_id:
            return render_template('anime.html', anime=anime,
                                   categories=categories, catg=catg,
                                   username=login_session['username'],
                                   allowmodify='true')
        return render_template('anime.html', anime=anime,
                               categories=categories, catg=catg,
                               username=login_session['username'])

    else:
        return render_template('anime.html',
                               anime=anime,
                               categories=categories,
                               catg=catg)


@app.route('/edit/<int:anime_id>', methods=['GET', 'POST'])
def editAnime(anime_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    editedItem = session.query(Anime).filter_by(id=anime_id).one()

    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['desc']:
            editedItem.description = request.form['desc']
        editedItem.catg_id = request.form['catg']
        session.add(editedItem)
        session.commit()
        flash(editedItem.title+" has been updated successfully!")

    categories = session.query(Category).all()

    if 'user_id' in login_session:
        if login_session['user_id'] == editedItem.user_id:
            return render_template('edit.html', categories=categories,
                                   username=login_session['username'],
                                   anime=editedItem)
    else:
        return redirect(url_for('error'))


@app.route('/delete/<int:anime_id>', methods=['GET', 'POST'])
def deleteAnime(anime_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    animeToDelete = session.query(Anime).filter_by(id=anime_id).one()
    categories = session.query(Category).all()
    if request.method == 'POST':
        session.delete(animeToDelete)
        session.commit()
        catg = session.query(Category).filter_by(
            id=animeToDelete.catg_id).one()
        return redirect(url_for('showCatg', catg_id=catg.id))
    else:
        if 'user_id' in login_session:
            if login_session['user_id'] == animeToDelete.user_id:
                return render_template('delete.html',
                                       categories=categories,
                                       username=login_session['username'],
                                       anime=animeToDelete)
        else:
            return redirect(url_for('error'))


@app.route('/403')
def error():
    return render_template('403.html')


def getAllAnime():
    allanime = []
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    catgs = session.query(Category).all()
    for catg in catgs:
        animelist = session.query(Anime).filter_by(catg_id=catg.id).all()
        for anime in animelist:
            allanime.append(anime)

    allanime = list(reversed(allanime))

    return allanime


# Main part runs if there is no exceptions, from python interpretur
if __name__ == '__main__':
    app.secret_key = 'super_secure'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
