from flask import render_template, flash, redirect, g, request
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

from app import app, host, port, user, passwd, db
from app.helpers.database import con_db
from forms import LoginForm

import urllib
import urllib2
import json
import requests

import mapquest_utils 

# To create a database connection, add the following
# within your view functions:
# con = con_db(host, port, user, passwd, db)


# ROUTING/VIEW FUNCTIONS

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

#=====================================
#Main Page:
#=====================================
        
@app.route('/', methods = ['GET', 'POST'])    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Start at"' + str(form.start.data) +'End at"' + str(form.end.data) )
	#print form.start, form.end,"#################",form.end.data
	#g['formstart'] = form.start
	#g['formend'] = form.end
        
	
    

#--------------------------------
#convert start/end to lat/long
#--------------------------------	
	start=form.start.data
	end=form.end.data
#--------------------------------	
#call Rick's api
#--------------------------------	
	url_base='http://insight.seeger.net:5000/v1/places'
	url=url_base
	
	headers = {'content-type': 'application/json'}
	response=requests.post(url, headers=headers)#request
	jsonRcv = response.text
	jsonObj = json.loads(jsonRcv)#parse result
	print json.dumps(jsonObj, indent=4, sort_keys=True)

#--------------------------------
#convert Ricks' data to a format mapquest likes
#--------------------------------

	ricklist=[]
        placenames=[]
	for i in range(len(jsonObj["places"])):
		ricklist.append(str(jsonObj["places"][i]['lat'])+"  " +str(jsonObj["places"][i]['lon']))
                placenames.append(jsonObj["places"][i]['name'])


#--------------------------------	
#run Mapquest Route matrix 
#and calculate time off route
#--------------------------------
        mquest=mapquest_utils.mapquest()
        startlist=[str(start)]
	endlist=[str(end)]

        timeoff=mquest.timeoffroute(ricklist,startlist,endlist)
        
#--------------------------------
#store in new form
#--------------------------------

#--------------------------------	
#render template with new form.
#--------------------------------
        '''
        #url = "..."
        #params = {'x':5, 'y':'Some place name'}
        #fullurl = url + '?' + urlencode(params)
        '''
        
#return render_template('results.html',timeoff=timeoff,places=placenames,fulljson=urllib.urlencode("this is a string"))
        return render_template('results.html',timeoff=timeoff,places=placenames)
#return redirect('/results')
    else:
        return render_template('login.html', title = 'miWay',form = form)





###########################################################
@app.route('/map', methods = ['GET'])
def maps():
    tmp = request.args.get("x")
    print tmp
    

    #return request.args.get("x")
    return render_template('home.html')

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

##########################################################
# @app.route('/results',methods=['GET','POST'])
# def results():
	
#     user = { 'nickname': 'Miguel' } # fake user
#     posts = [ # fake array of posts
#         { 
#             'author': { 'nickname': 'John' }, 
#             'body': 'Beautiful day in Portland!' 
#         },
#         { 
#             'author': { 'nickname': 'Susan' }, 
#             'body': 'The Avengers movie was so cool!' 
#         }
#     ]
#     print '@@@@@@@@@@@@@@@@@@ g = ',g
#     return render_template("index.html",
#         title = 'Home',
#         user = user,
#         posts = posts)
