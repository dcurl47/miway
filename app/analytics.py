#apply ranking algorithm to phoenix results

import pandas as pd
from numpy import sqrt, exp
import utils

#---------------------------------------
#Ranking of results
#Currently based only on yelp rating
#and approximate position along route.
#---------------------------------------
def analytics(phoenixlist,nroute,partscore,sigma):

    dphoenix=pd.DataFrame(phoenixlist,columns=['id','name','ratings','lat','lon'])
            
    dphoenix['dist']=sqrt((dphoenix['lat']-dphoenix['lat'][0])**2+(dphoenix['lon']-dphoenix['lon'][0])**2)
    last=dphoenix.last_valid_index()
    totdist=sqrt((dphoenix['lat'][last]-dphoenix['lat'][0])**2+(dphoenix['lon'][last]-dphoenix['lon'][0])**2)

    dphoenix['frac']=dphoenix['dist']/totdist
    #-----------------------------
    #Calculate score
    #------------------------------
    dphoenix['score']=dphoenix.apply(myfunc,axis=1,mean=partscore,sig=sigma)
               
    dphoenix['strpos']=dphoenix['lat'].astype('str')+" "+dphoenix['lon'].astype('str')
    dphoenix['yelpos']=dphoenix['lat'].astype('str')+","+dphoenix['lon'].astype('str')
    #-----------------------------
    #Sort by score and removed
    #lowest scores
    #------------------------------
    dphoenix=dphoenix.sort(columns='score',ascending=False) #sort by score
                
    nplaces=len(dphoenix)
    if nplaces > nroute: #keep at most nroute number of results
        dphoenix=dphoenix.drop(dphoenix.index[nroute:])
        nplaces=nroute

    return dphoenix


#-------------------------------------------
#Function to assign higher weight to desired
#part of the route.
#-------------------------------------------
def myfunc(x,mean=0.5,sig=1.0):
    #global mean
    #global sig
    return exp(-((x['frac']-mean)/sig)**2/2)/(sig*2.506628)
