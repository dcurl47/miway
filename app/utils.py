#random functions that didn't fit anywhere else

from forms import LoginForm
from numpy import exp,sqrt
import urllib
import urllib2
import json
import requests

def query_rick_api(routenodes,category):

    url_base='http://insight.seeger.net:5000/v1/places'
    url=url_base
	
    headers = {'content-type': 'application/json'}
    #response=requests.post(url,nodes=routenodes, headers=headers)#request
    response=requests.post(url, headers=headers)#request
    jsonRcv = response.text
    jsonObj = json.loads(jsonRcv)#parse result
    #print json.dumps(jsonObj, indent=4, sort_keys=True)
    return jsonObj

def getnodes(mapjson,detail):

    if detail==0:  #Only route maneuvers are passed to Rick
        sizemap=len(mapjson['route']['legs'][0]['maneuvers'])
        routenodes=[]
        for i in range(sizemap):
            lat=mapjson['route']['legs'][0]['maneuvers'][i]['startPoint']['lat']
            lon=mapjson['route']['legs'][0]['maneuvers'][i]['startPoint']['lng']
            node=(lat,lon)
            routenodes.append(node)
    elif detail==1:  #Detailed route lat/lons are passed to Rick.
        lat=jsonobj['route']['shape']['shapePoints'][0::2]
        lon=jsonobj['route']['shape']['shapePoints'][0::1]
        routenodes=zip(lat,lon)

    return routenodes

def mkgoogleurls(startlist,endlist,locations):

    gmaps_base="https://www.google.com/maps/dir/"
    gmaps_start=[w.replace('  ',',') for w in startlist]
    gmaps_start=[w.replace(' ','+') for w in gmaps_start]
     
    gmaps_base=gmaps_base+gmaps_start[0]#+"/"
    gmaps_end=[w.replace('  ',',') for w in endlist]
    gmaps_end=[w.replace(' ','+') for w in gmaps_end]
    gmaps_urls=[]
    nplaces=len(locations)
    for i in range(nplaces):
        gmaps_urls.append(gmaps_base)
    for i in range(nplaces):
        gmaps_urls[i]=gmaps_urls[i]+"/"+locations[i]+"/"+gmaps_end[0]
            
        #print "GMAPS URLS:",gmaps_urls
    return gmaps_urls




def getpartscore(routepart):
    
    if routepart=='beginning':
        partscore=0.1
    if routepart=='middle':
        partscore=0.5
    if routepart=='end':
        partscore=0.9
    return partscore
    
def convertformat(dphoenix):
    
    ricklist=dphoenix['strpos']
    ricklist=list(ricklist.values)
    ratings=dphoenix['ratings']
    ratings=list(ratings.values)
    yelp_names=dphoenix['name']
    yelp_names=list(yelp_names.values)
    rickyelp=dphoenix['yelpos']
    rickyelp=list(rickyelp.values)
    yelp_location=rickyelp
    

    return ricklist,ratings,yelp_names,rickyelp,yelp_location


def myfunc(x,mean=0.5,sig=1.0):
    #global mean
    #global sig
    return exp(-((x['frac']-mean)/sig)**2/2)/(sig*2.506628)
