#=========================================
#This file is only for testing purposes
#=========================================


from mapquest_utils import *


start='Menlo Park, CA'
end='Kirkwood, CA'


#loclist=["Kirkwood, CA", "Los Angeles, CA", "San Diego, CA", "Las Vegas, NV", "Portland, OR", "Salt Lake City, UT","Redmond, WA","Santa Barbara, CA","Riverside, CA","Eureka,CA","Medford,OR"]

loclist=["Chevron Pollock Pines, CA", "Los Angeles, CA", "San Diego, CA", "Las Vegas, NV", "Portland, OR", "Salt Lake City, UT","Redmond, WA","Santa Barbara, CA","Riverside, CA","Eureka,CA","Medford,OR"]

locations = '{locations: '+str(loclist)+', options: {allToAll:false}}'

print locations
mquest=mapquest()

 
# # make request
# response = mquest.onetomany(locations)
# ==============

# # parse result
# jsonObj = json.loads(jsonRcv)
# #print json.dumps(jsonObj, indent=4, sort_keys=True)

check=mquest.getonetomany(loclist)
startlist=["Kirkwood, CA"]
endlist=["Menlo Park, CA"]

time=mquest.timeoffroute(loclist,startlist,endlist)
 
