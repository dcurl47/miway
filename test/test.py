import urllib
import urllib2
import pycurl, cStringIO, json
import pandas as pd
import pdb

def query2json(url):
        # CREATE BUFFER AND CURL OBJECTS
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        
        # COLLECT URL DATA & WRITE TO BUFFER
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()

        # LOAD INTO JSON OBJECT
        return json.loads(buf.getvalue())


url2="http://www.mapquestapi.com/directions/v2/route?key=Fmjtd%7Cluur2g68n5%2C2x%3Do5-9a8gqr&from=Lancaster,PA&to=York,PA&to=Lancaster,PA&callback=renderNarrative"
tst = query2json(url2)

tst_df = pd.DataFrame(tst)






# ################################################
# url = 'http://www.someserver.com/cgi-bin/register.cgi'
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# values = {'name' : 'Michael Foord',
#           'location' : 'Northampton',
#           'language' : 'Python' }
# headers = { 'User-Agent' : user_agent }

# data = urllib.urlencode(values)
# req = urllib2.Request(url, data, headers)
# response = urllib2.urlopen(req)
# the_page = response.read()

# ###################################################
# #http GET request??

# REQUEST URL:

# myurl="http://www.mapquestapi.com/directions/v2/routematrix?key=Fmjtd%7Cluur2g68n5%2C2x%3Do5-9a8gqr"

# REQUEST BODY:
# {
#    locations: [
#       "York, PA",
#       "Lancaster, PA",
#       "Boalsburg, PA",
#       "Sunbury, PA"
#    ],
#    options: {
#       allToAll: false
#    }
# }
# ########################################################
