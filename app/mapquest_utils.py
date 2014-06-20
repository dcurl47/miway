import urllib
import urllib2
import json
import requests
from keys import keys
from operator import add


class mapquest():
    
    def __init__(self):
        self.key = keys.mapquest#'Fmjtd%7Cluur2g6znl%2C70%3Do5-9a8w9y'

    def onetoonedirections(self,start,end):
        url = 'http://www.mapquestapi.com/directions/v2/routematrix?key=' + self.key
        headers = {'content-type': 'application/json'}
        return requests.post(url, locations, headers=headers)
    

    def advanceddirections(self,start,end):
        url_base='http://www.mapquestapi.com/directions/v2/route?key='
        url_base=url_base+self.key
        
        
        url_mid='&ambiguities=ignore&avoidTimedConditions=false&doReverseGeocode=true&outFormat=json&routeType=fastest&timeType=1&enhancedNarrative=false&shapeFormat=raw&generalize=0&locale=en_US&unit=m&from='
        #start='Clarendon Blvd, Arlington, VA'
        url_mid2='&to='
        #end='2400 S Glebe Rd, Arlington, VA'
        url_end='&drivingStyle=1&highwayEfficiency=21.0'

        url_final=url_base + url_mid + start + url_mid2 + end + url_end
        url_final=url_final.replace(" ","%20")
        #print url_final
        return urllib2.urlopen(url_final)

    def onetomany(self,locations):
        #url_base=
        url = 'http://www.mapquestapi.com/directions/v2/routematrix?key=' + self.key
        headers = {'content-type': 'application/json'}
        return requests.post(url, locations, headers=headers)
        


    def timeoffroute(self,ricklist,startlist,endlist):
        #time off-route and distance along route
        strick=startlist+ricklist
        endrick=endlist+ricklist
        fidroute=startlist+endlist
        
        startjson=self.getonetomany(strick)
        endjson=self.getmanytoone(endrick)
        fidjson=self.getonetomany(fidroute)

        totaltime=map(add,startjson['time'],endjson['time'])
        fidtime=fidjson['time'][1]

        fiddist=fidjson['distance'][1]
        totaldist=startjson['distance']
        
        toffroute=[x-fidtime for x in totaltime]
        fracoffroute=[x/fiddist for x in totaldist]

        #Round-off and convert units

        toffroute=[0 if x<0 else x for x in toffroute]
        toffroute=[int(x/60.) for x in toffroute]  #convert to minutes

        fracoffroute=[float(int(x*100)) for x in fracoffroute]
        fiddist=int(10*fiddist)/10.
                      
        return toffroute,fracoffroute,fiddist,fidtime


        
    def getonetomany(self,ricklist):

        locations = '{locations: '+str(ricklist)+', options: {allToAll:false}}'
        mapresponse = self.onetomany(locations)
	jsonmap = mapresponse.text

	jsonObj = json.loads(jsonmap)
	#print json.dumps(jsonObj, indent=4, sort_keys=True)
        return jsonObj

    def getmanytoone(self,ricklist):

        locations = '{locations: '+str(ricklist)+', options: {manyToOne:true}}'
        mapresponse = self.onetomany(locations)
	jsonmap = mapresponse.text

	jsonObj = json.loads(jsonmap)
	#print json.dumps(jsonObj, indent=4, sort_keys=True)
        return jsonObj



    ##################################################
    #mquest=mapquest()
    #response=mquest.advanceddirections("kirkwood, ca","cupertino,ca")
    #jsonobj=json.loads(response.read())
