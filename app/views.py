from flask import render_template, flash, redirect
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

from app import app, host, port, user, passwd, db
from app.helpers.database import con_db
from forms import LoginForm

# To create a database connection, add the following
# within your view functions:
# con = con_db(host, port, user, passwd, db)


# ROUTING/VIEW FUNCTIONS
@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    posts = [ # fake array of posts
        { 
            'author': { 'nickname': 'John' }, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': { 'nickname': 'Susan' }, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)

######################################

@app.route('/results')
def results():
    user = { 'nickname': 'Miguel' } # fake user
    posts = [ # fake array of posts
        { 
            'author': { 'nickname': 'John' }, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': { 'nickname': 'Susan' }, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)
        
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Start at"' + str(form.start.data) +'End at"' + str(form.end.data) )
        #return redirect('/index')
    
    else:
        return render_template('login.html', title = 'Sign In',form = form)



@app.route('/map')
def maps():
    #Receive form from index.html
    start=request.form("start","")
    end=request.form("end","")
    place=request.form("place","")
    print "START = ",start,"  END = ",end,"  PLACE = ",place    
    #Create JSON
    #Send to Rick
    #Receive list in JSON format
    #Return list of choices for user

@app.route('/home')
def home():
    # Renders home.html.
    return render_template('home.html')

@app.route('/slides')
def about():
    # Renders slides.html.
    return render_template('slides.html')

@app.route('/author')
def contact():
    # Renders author.html.
    return render_template('author.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
