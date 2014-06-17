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

	#g['formstart'] = form.start
	#g['formend'] = form.end
        
	
#--------------------------------
#convert start/end to lat/long
#--------------------------------	
	start=form.start.data
	end=form.end.data
        category=form.place.data
        
        #startlat= jsonobj['route']['locations'][0]['latLng']['lat']
        #endlat= jsonobj['route']['locations'][1]['latLng']['lat']
#--------------------------------
#call Mapquest API and extract
#route nodes
#--------------------------------
        mquest=mapquest_utils.mapquest()
	mapresponse=mquest.advanceddirections(start,end)
        mapjson=json.loads(mapresponse.read())

        detail=0
        if detail==0:  #Only route maneuvers are passed to Rick
            sizemap=len(mapjson['route']['legs'][0]['maneuvers'])
            routenodes=[]
            for i in range(sizemap):
                lat=mapjson['route']['legs'][0]['maneuvers'][0]['startPoint']['lat']
                lon=mapjson['route']['legs'][0]['maneuvers'][0]['startPoint']['lng']
                node=(lat,lon)
                routenodes.append(node)
        elif detail==1:  #Detailed route lat/lons are passed to Rick.
            lat=jsonobj['route']['shape']['shapePoints'][0::2]
            lon=jsonobj['route']['shape']['shapePoints'][0::1]
            routenodes=zip(lat,lon)

#--------------------------------	
#call my database (yelp_phoenix)
#--------------------------------	
#if phoenix:
            
#--------------------------------	
#call Rick's api
#--------------------------------	
	url_base='http://insight.seeger.net:5000/v1/places'
	url=url_base
	
	headers = {'content-type': 'application/json'}
	#response=requests.post(url,nodes=routenodes, headers=headers)#request
        response=requests.post(url, headers=headers)#request
	jsonRcv = response.text
	jsonObj = json.loads(jsonRcv)#parse result
	print json.dumps(jsonObj, indent=4, sort_keys=True)

#--------------------------------
#convert Ricks' data to a format mapquest likes
#--------------------------------

	ricklist=[]
        placenames=[] 
        nplaces=len(jsonObj["places"])
	for i in range(nplaces):
		ricklist.append(str(jsonObj["places"][i]['lat'])+\
                                "  " +str(jsonObj["places"][i]['lon']))
                placenames.append(jsonObj["places"][i]['name'])


        rickyelp=[w.replace('  ',',') for w in ricklist]


        

#------------------------------------
#get Yelp reviews and business urls.
#------------------------------------
        limit=1
        
        ratings=[]
        yelp_urls=[]
        yelp_names=[]
        yelp_location=[]
        for i in range(nplaces):
            point=rickyelp[i]
            yelp_response=yelp_search.process_request(point,limit,category)
            if yelp_response:
                ratings.append(yelp_response['businesses'][0]['rating'])
                yelp_urls.append(yelp_response['businesses'][0]['url'])
                yelp_names.append(yelp_response['businesses'][0]['name'])
                tmp=str(yelp_response['businesses'][0]['location']['address'][0]) + "  " + str(yelp_response['businesses'][0]['location']['city']) + ", " + str(yelp_response['businesses'][0]['location']['state_code']) + ", " + str(yelp_response['businesses'][0]['location']['country_code'])
                tmp=tmp.replace('  ','+')
                tmp=tmp.replace(' ','+')
                yelp_location.append(tmp)
                print "YELP LOCATION: ",yelp_location[i]

#===========================================================
#Analytics to choose which places to get time off-route for
#and which to display on website
#===========================================================
#variables: rating, distance along route,category

#place score=



#-----------------------------------	
#run Mapquest Route matrix 
#and calculate time off-route, distance
#along route and shortest route
#-----------------------------------
        mquest=mapquest_utils.mapquest()
        startlist=[str(start)]
	endlist=[str(end)]

        timeoff,fracoff,routelength,routetime = mquest.timeoffroute(ricklist,startlist,endlist)

        timeoff=[0 if x<0 else x for x in timeoff]
        timeoff=[int(x/60.) for x in timeoff]  #convert to minutes

        fracoff=[int(x*100) for x in fracoff]
        routehours=routetime//3600
        routemins=(routetime%3600)//60
        routelength=int(10*routelength)/10.
#------------------------------------
#make Google maps urls.
#------------------------------------
        gmaps_base="https://www.google.com/maps/dir/"
        gmaps_start=[w.replace('  ',',') for w in startlist]
        gmaps_start=[w.replace(' ','+') for w in gmaps_start]
        
        gmaps_base=gmaps_base+gmaps_start[0]#+"/"
        gmaps_end=[w.replace('  ',',') for w in endlist]
        gmaps_end=[w.replace(' ','+') for w in gmaps_end]
        gmaps_urls=[]
        for i in range(nplaces):
            gmaps_urls.append(gmaps_base)
        for i in range(nplaces):
            #gmaps_urls[i]=gmaps_urls[i]+"/"+rickyelp[i]+"/"+gmaps_end[0]
            gmaps_urls[i]=gmaps_urls[i]+"/"+yelp_location[i]+"/"+gmaps_end[0]
            
            print "GMAPS URLS:",gmaps_urls
            
#return render_template('results.html',timeoff=timeoff,places=placenames,fulljson=urllib.urlencode("this is a string"))

        

        return render_template('results.html',timeoff=timeoff,fracoff=fracoff,routelength=routelength,routehours=routehours,routemins=routemins,places=yelp_names,ratings=ratings,yelp_urls=yelp_urls,gmaps_urls=gmaps_urls)
    #return render_template('results.html',timeoff=timeoff,places=placenames,ratings=ratings,yelp_urls=yelp_urls,gmaps_urls=gmaps_urls)
#return redirect('/results')
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
