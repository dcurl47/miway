"""Command line interface to the Yelp Search API."""

import json
import oauth2
import optparse
import urllib
import urllib2

from keys import keys
import os
import pandas as pd

consumer_key = keys.yelp_cons_key
consumer_secret = keys.yelp_cons_sec
token = keys.yelp_tok
token_secret = keys.yelp_tok_sec
 

# Setup URL params from options
url_params = {}
def process_request(point,limit, category,radius=100):
    url_params = {}
    url_params['ll'] = point 
    url_params['limit'] = limit
    #url_params['category_filter'] = category
    url_params['term']=category
    url_params['radius_filter']=radius
    response = request('api.yelp.com','/v2/search', url_params, consumer_key, consumer_secret, token, token_secret)
    return response

def process_request_id(point,limit):
    url_params = {}
    url_params['id'] = point 
    url_params['limit'] = limit
    response = request('api.yelp.com','/v2/search', url_params, consumer_key, consumer_secret, token, token_secret)
    return response


def request(host, path, url_params, consumer_key, consumer_secret, token, token_secret):
  """Returns response for API request."""
  # Unsigned URL
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)
  url = 'http://%s%s?%s' % (host, path, encoded_params)
  #print 'URL: %s' % (url,)

  # Sign the URL
  consumer = oauth2.Consumer(consumer_key, consumer_secret)
  oauth_request = oauth2.Request('GET', url, {})
  oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                        'oauth_timestamp': oauth2.generate_timestamp(),
                        'oauth_token': token,
                        'oauth_consumer_key': consumer_key})

  token = oauth2.Token(token, token_secret)
  oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
  signed_url = oauth_request.to_url()
  #print 'Signed URL: %s\n' % (signed_url,)

  # Connect
  try:
    conn = urllib2.urlopen(signed_url, None)
    try:
      response = json.loads(conn.read())
    finally:
      conn.close()
  except urllib2.HTTPError, error:
    response = json.loads(error.read())

  return response

def get_yelp_info(limit,locations,category):
  nroute=25
  allinfo=[[],[],[],[]]
  ratings=[]
  yelp_urls=[]
  yelp_names=[]
  yelp_location=[]
  nplaces=len(locations)
  for i in range(nplaces):
    
    point=locations[i]
    radius=50
    yelp_response=process_request(point,limit,category,radius)
    #print "YELP_RESPONSE = ", len(yelp_response)
    tries=0
    
    while not yelp_response['businesses'] and tries<2:
      print "IN WHILE LOOP, i = ",i
      radius+=50
      tries+=1
      yelp_response=process_request(point,limit,category,radius)
    
    
    if  yelp_response['businesses']:
      allinfo[0].append(yelp_response['businesses'][0]['rating'])
      allinfo[1].append(yelp_response['businesses'][0]['url'])
      allinfo[2].append(yelp_response['businesses'][0]['name'])
      
      if yelp_response['businesses'][0]['location']['address']:
        tmp=str(yelp_response['businesses'][0]['location']['address'][0]) + "  " + str(yelp_response['businesses'][0]['location']['city']) 
      else:
        tmp=str("Address not Found")
      
      #tmp=str(yelp_response['businesses'][0]['location']['address'][0]) + "  " + str(yelp_response['businesses'][0]['location']['city']) + ", " + str(yelp_response['businesses'][0]['location']['state_code']) + ", " + str(yelp_response['businesses'][0]['location']['country_code'])
      tmp=tmp.replace('  ','+')
      tmp=tmp.replace(' ','+')
      #yelp_location.append(tmp)
      allinfo[3].append(tmp)
      #print "AAAAAAAAAAAAAAAAAAAAAAAAAAA", allinfo
  dphoenix=pd.DataFrame(allinfo,index=['ratings','url','names','location'])
  #print dphoenix.info
  dphoenix=dphoenix.transpose()
  dphoenix=dphoenix.drop_duplicates()
  dphoenix=dphoenix.drop(dphoenix.index[nroute:])
  #print dphoenix.info
  (yelp_location,yelp_names,yelp_urls,ratings) = convertformat(dphoenix)
      
  return yelp_location,yelp_names,yelp_urls,ratings


def convertformat(dphoenix):
    
    yelp_location=dphoenix['location']
    yelp_location=list(yelp_location.values)
    ratings=dphoenix['ratings']
    ratings=list(ratings.values)
    yelp_names=dphoenix['names']
    yelp_names=list(yelp_names.values)
    yelp_urls=dphoenix['url']
    yelp_urls=list(yelp_urls.values)
    
    return yelp_location,yelp_names,yelp_urls,ratings








#response = request(options.host, '/v2/search', url_params, options.consumer_key, options.consumer_secret, options.token, options.token_secret)
#print json.dumps(response, sort_keys=True, indent=2)
  
