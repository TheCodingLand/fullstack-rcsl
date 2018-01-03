import redis
from operator import itemgetter
import time
import pytz
from datetime import datetime

from eventmanager import services


r = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=2)


def getAddedCalls():
    for key in r.scan_iter(match='*'):     
        try:
            c = r.hgetall(key)
        except redis.exceptions.ResponseError:
            pass
        s = services.Services(c)
        if s.done== True:
            r.delete(key)
            
#quick cleaup as this key is only used for real time data            

    
while True:
    getAddedCalls()
    

        
    
