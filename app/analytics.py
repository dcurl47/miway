#apply ranking algorithm to phoenix results

import pandas as pd
from numpy import sqrt
import utils

def analytics(phoenixlist,nroute,partscore,sigma):

    dphoenix=pd.DataFrame(phoenixlist,columns=['id','name','ratings','lat','lon'])
            
    dphoenix['dist']=sqrt((dphoenix['lat']-dphoenix['lat'][0])**2+(dphoenix['lon']-dphoenix['lon'][0])**2)
    last=dphoenix.last_valid_index()
    totdist=sqrt((dphoenix['lat'][last]-dphoenix['lat'][0])**2+(dphoenix['lon'][last]-dphoenix['lon'][0])**2)

    dphoenix['frac']=dphoenix['dist']/totdist
    dphoenix['score']=dphoenix.apply(utils.myfunc,axis=1,mean=partscore,sig=sigma)
               
    dphoenix['strpos']=dphoenix['lat'].astype('str')+" "+dphoenix['lon'].astype('str')
    dphoenix['yelpos']=dphoenix['lat'].astype('str')+","+dphoenix['lon'].astype('str')
    dphoenix=dphoenix.sort(columns='score',ascending=False) #sort by score
                
    nplaces=len(dphoenix)
    if nplaces > nroute: #keep at most nroute number of results
        dphoenix=dphoenix.drop(dphoenix.index[nroute:])
        nplaces=nroute

    return dphoenix
