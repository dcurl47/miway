from forms import LoginForm

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
            lat=mapjson['route']['legs'][0]['maneuvers'][0]['startPoint']['lat']
            lon=mapjson['route']['legs'][0]['maneuvers'][0]['startPoint']['lng']
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
