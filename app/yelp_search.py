"""Command line interface to the Yelp Search API."""

import json
import oauth2
import optparse
import urllib
import urllib2

from keys import keys
import os


consumer_key = keys.yelp_cons_key
consumer_secret = keys.yelp_cons_sec
token = keys.yelp_tok
token_secret = keys.yelp_tok_sec
 

# Setup URL params from options
url_params = {}
def process_request(point,limit, category):
    url_params = {}
    url_params['ll'] = point 
    url_params['limit'] = limit
    #url_params['category_filter'] = category
    url_params['term']=category
    #url_params['radius_filter']=100
    response = request('api.yelp.com','/v2/search', url_params, consumer_key, consumer_secret, token, token_secret)
    return response

def request(host, path, url_params, consumer_key, consumer_secret, token, token_secret):
  """Returns response for API request."""
  # Unsigned URL
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)
  url = 'http://%s%s?%s' % (host, path, encoded_params)
  print 'URL: %s' % (url,)

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
  print 'Signed URL: %s\n' % (signed_url,)

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

#response = request(options.host, '/v2/search', url_params, options.consumer_key, options.consumer_secret, options.token, options.token_secret)
#print json.dumps(response, sort_keys=True, indent=2)
  
