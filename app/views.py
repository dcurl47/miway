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
import analytics
import pandas as pd
from numpy import sqrt


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)

#=====================================
#Main Page:
#=====================================
        
@app.route('/', methods = ['GET', 'POST'])    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    limit=1   #number of results per Yelp api query.
    nroute=25  #Maximum number of routes to calculate
    sigma=0.3  #to be used in ranking of results
    phoenix=True #Use rick_api if False, phoenix api if True



# ---------------------------------------------
# Read the form from login.html
# ---------------------------------------------

    form = LoginForm()
    if form.validate_on_submit():
        flash('Start at"' + str(form.start.data) +'End at"' + str(form.end.data) )
        
	start=form.start.data
	end=form.end.data
        category=form.place.data
        routepart=form.partroute.data
        
#--------------------------------
# Convert user preference for when to stop
# to a number (to be used in the ranking score)
#--------------------------------
        partscore=utils.getpartscore(routepart)
        partsig=sigma 
        
        
#--------------------------------
#call Mapquest API and extract
#route nodes
#--------------------------------
        mquest=mapquest_utils.mapquest()
	mapresponse=mquest.advanceddirections(start,end)
        mapjson=json.loads(mapresponse.read())

        detail=0 #0: nodes=steps in the directions
                 #1: much finer resolution, based on full route path.
        routenodes = utils.getnodes(mapjson,detail)
#--------------------------------	
#call my test database (yelp_phoenix)
#and get coarse batch of locations.
#--------------------------------	

        if phoenix:
            thick=0.03
            if category=="restaurant":
                thick=0.01
            if category=="pharmacy":
                thick=0.9
            
            phoenixlist=query_yelp_db.querybox(routenodes,category,thick)
        
            if len(phoenixlist)<1:
                flash('Try again!"' + str(form.start.data) +'End at"' + str(form.end.data) )
                notfound=["Sorry, but nothing was found along your route.","Perhaps, you should go elsewhere."]
                return render_template('login.html', title = 'try again!',form = form,notfound=notfound)

#--------------------------------	
#phoenix ranking analytics
#--------------------------------

            dphoenix=analytics.analytics(phoenixlist,nroute,partscore,sigma)
#--------------------------------	
#convert phoenix results to
#previous format
#--------------------------------
            (ricklist,ratings,yelp_names,rickyelp,yelp_location,yelp_id)=utils.convertformat(dphoenix)
            
        else:
#--------------------------------	
#call Rick's api
#--------------------------------	
            jsonObj=utils.query_rick_api(routenodes,category)
            #print json.dumps(jsonObj, indent=4, sort_keys=True)
#--------------------------------
#convert Ricks data to formats mapquest and yelp like
#--------------------------------

            ricklist=[]
            placenames=[] 
            nplaces=len(jsonObj["places"])
            for i in range(nplaces):
		ricklist.append(str(jsonObj["places"][i]['lat'])+\
                                "  " +str(jsonObj["places"][i]['lon']))
                placenames.append(jsonObj["places"][i]['name'])
            rickyelp=[w.replace('  ',',') for w in ricklist]
                   

#---------------------------------------------
#end of separation between rick and phoenix.
#---------------------------------------------

#------------------------------------
#given location and category,
#get Yelp reviews and business urls.
#------------------------------------

        (yelp_location,yelp_names,yelp_urls,ratings)=yelp_search.get_yelp_info(limit,rickyelp,category)

        
#--------------------------------------------------
#run Mapquest Route matrix to get time off-route, 
#  distance along route and shortest route
#--------------------------------------------------

        mquest=mapquest_utils.mapquest()
        startlist=[str(start)]
	endlist=[str(end)]
        
        timeoff,fracoff,routelength,routetime,startgmap,endgmap,locgmap = mquest.timeoffroute(ricklist,startlist,endlist)
        routehours=routetime//3600
        routemins=(routetime%3600)//60

#------------------------------------
#make Google maps urls.
#------------------------------------
        
        gmaps_urls=utils.mkgoogleurls(startlist,endlist,yelp_location)

#------------------------------------
#Render template
#------------------------------------
        
        
        return render_template('results.html',timeoff=timeoff,fracoff=fracoff,routelength=routelength,routehours=routehours,routemins=routemins,places=yelp_names,ratings=ratings,yelp_urls=yelp_urls,gmaps_urls=gmaps_urls,start=startgmap,end=endgmap,locgmap=locgmap)
    
    else:
        return render_template('login.html', title = 'Jaunt',form = form)





###########################################################
@app.route('/map', methods = ['GET'])
def maps():

    return render_template('map.html')


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


