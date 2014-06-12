import urllib
import urllib2
import json
import requests


class googlemaps():

    def __init__(self):
        self.key='AIzaSyAjcoHKuP8mS6OsIcjkRCypwkL-Cb5WccQ'

        
    def directions(self,origin,destination,waypoints=None):
        #routelist includes origin, waypoints and destination
        url_base='https://maps.googleapis.com/maps/api/directions/json?'

https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=AIzaSyBpmTdxyUqC1X914CKyT1b78WABMoex6eM

AIzaSyAjcoHKuP8mS6OsIcjkRCypwkL-Cb5WccQ
AIzaSyAjcoHKuP8mS6OsIcjkRCypwkL-Cb5WccQ
AIzaSyAjcoHKuP8mS6OsIcjkRCypwkL-Cb5WccQ
