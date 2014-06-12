import urllib
import urllib2
import json
import requests
from operator import add

class mapquest():
    
    def __init__(self):
        self.key = 'Fmjtd%7Cluur2g6znl%2C70%3Do5-9a8w9y'

    def onetomany(self,locations):
        #url_base=
        url = 'http://www.mapquestapi.com/directions/v2/routematrix?key=' + self.key
        headers = {'content-type': 'application/json'}
        return requests.post(url, locations, headers=headers)
        


    def timeoffroute(self,ricklist,startlist,endlist):

        strick=startlist+ricklist
        endrick=endlist+ricklist
        fidroute=startlist+endlist
        
        startjson=self.getonetomany(strick)
        endjson=self.getonetomany(endrick)
        fidjson=self.getonetomany(fidroute)

        totaltime=map(add,startjson['time'],endjson['time'])
        fidtime=fidjson['time'][1]

        toffroute=[x-fidtime for x in totaltime]

        return toffroute
        
    def getonetomany(self,ricklist):

        locations = '{locations: '+str(ricklist)+', options: {allToAll:false}}'
        
	#mquest=self.mapquest()
# make request
	mapresponse = self.onetomany(locations)
	jsonmap = mapresponse.text

# parse result
	jsonObj = json.loads(jsonmap)
	#print json.dumps(jsonObj, indent=4, sort_keys=True)
        return jsonObj
