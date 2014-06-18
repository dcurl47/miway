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
import yelp_search
import query_yelp_db  #for phoenix db
import utils
import pandas as pd
# To create a database connection, add the following
# within your view functions:
# con = con_db(host, port, user, passwd, db)

#=====================================
#Main Page:
#=====================================
        
@app.route('/', methods = ['GET', 'POST'])    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    phoenix=False
    form = LoginForm()
    if form.validate_on_submit():
        flash('Start at"' + str(form.start.data) +'End at"' + str(form.end.data) )
        
	start=form.start.data
	end=form.end.data
        category=form.place.data
        
#--------------------------------
#call Mapquest API and extract
#route nodes
#--------------------------------
        mquest=mapquest_utils.mapquest()
	mapresponse=mquest.advanceddirections(start,end)
        mapjson=json.loads(mapresponse.read())

        detail=0
        routenodes = utils.getnodes(mapjson,detail)
#--------------------------------	
#call my test database (yelp_phoenix)
#--------------------------------	

#if phoenix:
        thick=0.01
        phoenixlist=query_yelp_db.querybox(routenodes,category,thick)
        
        #needed: ricklist,yelp_urls,yelp_names,yelp_locations (or rickyelp),ratings
        #ricklist: 'lat  lon'
        #rickyelp: 'lat, lon'
        #yelp_names =

#--------------------------------	
#phoenix analytics
#--------------------------------
        dphoenix=pd.DataFrame(phoenixlist)
        print "COLUMNS  ",
        if len(dphoenix.columns)!=0:
            dphoenix=dphoenix.sort(column=1) #sort by rating
            yelp_names=dphoenix[0].values
            dphoenix[2]=dphoenix[2].astype('str')
            dphoenix[3]=dphoenix[3].astype('str')
        
        #b[2]+", "+b[3]
            ricklist=dphoenix[2]+" "+dphoenix[3]
            rickyelp=dphoenix[2]+","+dphoenix[3]
            yelp_location=rickyelp
        
        #else:
#--------------------------------	
#call Rick's api
#--------------------------------	
        jsonObj=utils.query_rick_api(routenodes,category)
        #print json.dumps(jsonObj, indent=4, sort_keys=True)
#--------------------------------
#convert Ricks' data to formats mapquest and yelp like
#--------------------------------

	ricklist=[]
        placenames=[] 
        nplaces=len(jsonObj["places"])
	for i in range(nplaces):
		ricklist.append(str(jsonObj["places"][i]['lat'])+\
                                "  " +str(jsonObj["places"][i]['lon']))
                placenames.append(jsonObj["places"][i]['name'])
        rickyelp=[w.replace('  ',',') for w in ricklist]
        print "RICKYELP = ",rickyelp

        print "RICKLIST = ",ricklist        

#------------------------------------
#given location and category,
#get Yelp reviews and business urls.
#------------------------------------
        limit=1
        (yelp_location,yelp_names,yelp_urls,ratings)=yelp_search.get_yelp_info(limit,rickyelp,category)
        print "YELP LOCATION: ",yelp_location[i]

#===========================================================
#Analytics to choose which places to get time off-route for
#and which to display on website
#===========================================================
#variables: rating, distance along route,category,price

#place score=



#------------------------------------------------	
#run Mapquest Route matrix to get time off-route, 
#  distance along route and shortest route
#------------------------------------------------
        mquest=mapquest_utils.mapquest()
        startlist=[str(start)]
	endlist=[str(end)]
        timeoff,fracoff,routelength,routetime = mquest.timeoffroute(ricklist,startlist,endlist)
        routehours=routetime//3600
        routemins=(routetime%3600)//60

#------------------------------------
#make Google maps urls.
#------------------------------------
        
        gmaps_urls=utils.mkgoogleurls(startlist,endlist,yelp_location)

#------------------------------------
#Render template
#------------------------------------
            
        return render_template('results.html',timeoff=timeoff,fracoff=fracoff,routelength=routelength,routehours=routehours,routemins=routemins,places=yelp_names,ratings=ratings,yelp_urls=yelp_urls,gmaps_urls=gmaps_urls)
    
    else:
        return render_template('login.html', title = 'miWay',form = form)





###########################################################
@app.route('/map', methods = ['GET'])
def maps():
    tmp = request.args.get("x")
    print tmp
    

    #return request.args.get("x")
    return render_template('map.html')

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


# @app.route('/index')
# def index():
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
#     return render_template("index.html",
#         title = 'Home',
#         user = user,
#         posts = posts)


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
