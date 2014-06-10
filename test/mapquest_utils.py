import urllib
import urllib2
import json
import requests

class mapquest():
    
    def __init__(self):
        self.key = 'Fmjtd%7Cluur2g6znl%2C70%3Do5-9a8w9y'

    def onetomany(self,locations):
        url_base=url = 'http://www.mapquestapi.com/directions/v2/routematrix?key=' + self.key
        headers = {'content-type': 'application/json'}
        return requests.post(url, locations, headers=headers)
        

    #def addresstolatlong(self,locations):
