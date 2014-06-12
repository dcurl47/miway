import requests
import json

developerKey = 'Fmjtd%7Cluur2g6znl%2C70%3Do5-9a8w9y'
url = 'http://www.mapquestapi.com/directions/v2/routematrix?key=' + developerKey

# construct JSON
#payload = '{ locations: [ "Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA", "Sacramento, CA", "Las Vegas, NV", "Los Angeles, CA" ], options: { allToAll: false } }'

#payload = '{ locations: [ "Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA", "Sacramento, CA", "Las Vegas, NV", "Los Angeles, CA", "Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA", "Sacramento, CA", "Las Vegas, NV", "Los Angeles, CA","Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA", "Sacramento, CA", "Las Vegas, NV", "Los Angeles, CA","Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA", "Sacramento, CA", "Las Vegas, NV", "Los Angeles, CA" ], options: { allToAll: false } }'

#payload = '{ locations: [ "Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA", "Sacramento, CA", "Las Vegas, NV", "Los Angeles, CA", "Santa Cruz, CA","Berkeley, CA","Oakland,CA","Cupertino,CA","San Jose,CA","Los Gatos,CA","Fremont,CA","Hayward,CA","San Mateo,CA","Jackson, CA","South Lake Tahoe, CA","Reno, NV","Redwood City, CA","Atherton,CA","Los Altos, CA","San Carlos, CA" ], options: { allToAll: false } }'

payload = '{ locations: [ "Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA", "Sacramento, CA", "Las Vegas, NV", "Los Angeles, CA", "Santa Cruz, CA","Berkeley, CA","Oakland,CA","Cupertino,CA","San Jose,CA","Los Gatos,CA","Fremont,CA","Hayward,CA","San Mateo,CA","Jackson, CA","South Lake Tahoe, CA","Reno, NV","Redwood City, CA","Atherton,CA","Los Altos, CA","San Carlos, CA","Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA", "Sacramento, CA", "Las Vegas, NV", "Los Angeles, CA", "Santa Cruz, CA","Berkeley, CA","Oakland,CA","Cupertino,CA","San Jose,CA","Los Gatos,CA","Fremont,CA","Hayward,CA","San Mateo,CA","Jackson, CA","South Lake Tahoe, CA","Reno, NV","Redwood City, CA","Atherton,CA","Los Altos, CA","San Carlos, CA","Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA", "Sacramento, CA", "Las Vegas, NV", "Los Angeles, CA", "Santa Cruz, CA","Berkeley, CA","Oakland,CA","Cupertino,CA","San Jose,CA","Los Gatos,CA","Fremont,CA","Hayward,CA","San Mateo,CA","Jackson, CA","South Lake Tahoe, CA","Reno, NV","Redwood City, CA","Atherton,CA","Los Altos, CA","San Carlos, CA","Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA", "Sacramento, CA", "Las Vegas, NV", "Los Angeles, CA", "Santa Cruz, CA","Berkeley, CA","Oakland,CA","Cupertino,CA","San Jose,CA","Los Gatos,CA","Fremont,CA","Hayward,CA","San Mateo,CA","Jackson, CA","South Lake Tahoe, CA","Reno, NV","Redwood City, CA","Atherton,CA","Los Altos, CA","San Carlos, CA" ], options: { allToAll: false } }'

#payload = '{ locations: [ "Kirkwood, CA", "Palo Alto, CA", "San Francisco, CA", "Sunnyvale, CA","Redwood City, CA","Atherton,CA","Los Altos, CA","San Carlos, CA","Fremont,CA","Hayward,CA","San Mateo,CA"], options: { allToAll: false } }'

#payload = '{ locations: [ "Kirkwood, CA", "Palo Alto, CA"], options: { allToAll: false } }'

#payload = '{locations: ["Kirkwood, CA", "Los Angeles, CA", "San Diego, CA", "Las Vegas, NV", "Portland, OR", "Salt Lake City, UT","Redmond, WA","Santa Barbara, CA","Riverside, CA","Eureka,CA","Medford,OR"], options: { allToAll: false } }'
# set HTTP headers
headers = {'content-type': 'application/json'}

# make request
response = requests.post(url, payload, headers=headers)
jsonRcv = response.text

# parse result
jsonObj = json.loads(jsonRcv)
print json.dumps(jsonObj, indent=4, sort_keys=True)



