import redis
from operator import itemgetter
from django.core.exceptions import ObjectDoesNotExist


from django.core.exceptions import ObjectDoesNotExist
django.setup()
import time
import pytz
from datetime import datetime

from eventmanager import services


r = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=)

def getAddedCalls():
    for key in r.scan_iter(match='*'):     
        try:
            c = r.hgetall(key)
        except redis.exceptions.ResponseError:
            pass
        s = Services(c)
        if s.done== True:
            r.delete(key)
  
    
while True:
    getAddedCalls()
    time.sleep(0.0001)

        
    
