import yelp_search
import json
#python yelp_search.py --consumer_key="ttyV6ZPYVpkyCAc7YyCzow" --consumer_secret="soI3udODLTTtXImUvN8o2C45V64" --token="36hrQXMnjlO1HWOaH15i6FrYmtEl1DAp" --token_secret="gn0bDEdzVFj7ObnsHMzLY-pBih0" --point="38.851726,-120.019764"  -- 
limit=1
category="restaurant"
#term=""

yelp_response=yelp_search.process_request(point,limit,category)
#print json.dumps(response, sort_keys=True, indent=2)

#Location of turns
#jsonobj['route']['legs'][0]['maneuvers'][:]['startPoint']

# { "steps": [ { "lat" : 45.7, "lng" : 78.9 }, { ... } ] }
