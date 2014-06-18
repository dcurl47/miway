import pymysql
from numpy import sqrt
import pandas as pd

# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='yelp_phoenix')

# cur = conn.cursor()




#=====================================================
def querybox(nodes,category,proximity=0.01):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='yelp_phoenix')
    cur = conn.cursor()

    lat=[]
    lon=[]
    names=[]
    stars=[]
    url=[]
    

    nnodes=len(nodes)
    print "LENGTH OF NODES: ",nnodes
    print "NODES =", nodes
    a=[]
    for i in range(nnodes-1):
        if (nodes[i][0]<nodes[i+1][0] and nodes[i][1]<nodes[i+1][1]) or (nodes[i][0]>nodes[i+1][0] and nodes[i][1]>nodes[i+1][1]): 
            p1=nodes[i+1]
            p0=nodes[i]
        else:
            p1=nodes[i]
            p0=nodes[i+1]
            
        slope=getslope(p0,p1)
        dist=getdistance(p0,p1)
        offset=dist*proximity
        latoffset=proximity*slope
        lonoffset=proximity/slope
        latoffmax=p0[0]+latoffset
        latoffmin=p0[0]-latoffset
        lonoffmax=p0[1]+lonoffset
        lonoffmin=p0[1]-lonoffset
        lonmax=max(p1[1],p0[1])
        lonmin=min(p1[1],p0[1])
        latmax=max(p1[0],p0[0])
        latmin=min(p1[0],p0[0])

        
        querystring="SELECT name,stars,latitude,longitude FROM yelp_business WHERE categories LIKE \'%{0}%\' AND (longitude>(latitude-{1})*{2} + {3}) AND (longitude<(latitude-{4})*{5} + {6}) AND (longitude > {7}) AND (longitude < {8}) AND (latitude < {9}) AND (latitude > {10})".format(category,latoffmax,slope,lonoffmax,latoffmin,slope,lonoffmin,lonmin,lonmax,latmax,latmin)
                
        #print "QUERYSTRING = ",querystring
        cur.execute(querystring)
        r= cur.fetchall()
        a=a+list(r)
        print "LENGTH of r = ",len(r), "LENGTH of a = ",len(a)

   
        
    return  a 



def getslope(p0,p1):
    #convert to radians%
    if (p1[0]-p0[0]) !=0:
        s=(p1[1]-p0[1])/(p1[0]-p0[0])
    else: s=1000
    return s 

def getdistance(p0,p1):
    #WARNING: fix this to apply Haversine formula
    #convert to radians%
    return sqrt((p1[1]-p0[1])**2 + (p1[0]-p0[0])**2)


if __name__=="__main__":
    xlat=[]
    xlon=[]
    nodes=[(33.3,-111.78),(33.8,-112.18),(34.1,-111.8),(33.3,-111.78)]
    #nodes=[(33.8,-112.18),(34.1,-111.8)]
    #nodes=[(33.3,-111.78),(33.8,-112.18)]
    rr=querybox(nodes,"restaurant",0.01)
    for i in range(len(rr)):
        xlat.append(rr[i][2])
        xlon.append(rr[i][3])


#cur.close()
#conn.close()
