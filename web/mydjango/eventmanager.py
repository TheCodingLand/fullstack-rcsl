import redis
from operator import itemgetter
from django.core.exceptions import ObjectDoesNotExist

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mydjango.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()
import time
import pytz
from datetime import datetime

paris=pytz.timezone('Europe/Paris')
from graphqlendpoint.models import Agent, Agent_ot, Agent_unify,Event_ot, Call
r = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=0)

def formattime(datestr):
    try:
        dt = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S.%f')
    except:
        dt = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
    return dt


def getAddedCalls(delete):
    for key in r.scan_iter(match='*add*'):     
        try:
            c = r.hgetall(key)
        except redis.exceptions.ResponseError:
            pass
        id = c.get('id')
        call=Call.objects.update_or_create(ucid=id)[0]
        dt = formattime(c.get('timestamp'))
        ts = paris.localize(dt)
        call.start=ts
        call.save()
        if delete == True:
            r.delete(key)
            print ("removing : %s" % key)

def getCallsInfo(call, delete):
    id = call.ucid
    
    
    for a in r.scan_iter(match='*setcaller-*-%s*' % id):
        caller = r.hgetall(a)    
        call.origin=caller.get('data')
        call.save()
        if delete ==True:
            print("removing : %s" % a)
            r.delete(a)

    
    
    
    for a in r.scan_iter(match='*setdetails-*-%s*' % id):
        details = r.hgetall(a)    
        call.call_type=details.get('data')
        call.save()
        if delete ==True:
            print("removing : %s" % a)
            r.delete(a)
    d=[]
    
    for t in r.scan_iter(match='*-transfer-*-%s' % id):
        transf = r.hgetall(t)
        d.append(transf)
        if delete ==True:
            print("removing : %s" % t)
            r.delete(t)
        
    sortedlist = sorted(d, key=itemgetter('timestamp')) 
   
    for item in sortedlist:
        agent_unify = Agent_unify.objects.update_or_create(ext=item.get('data'))[0]
        agent_unify.save()
        call.primaryagent = agent_unify
        call.history = "%s -> %s" % (call.history,agent_unify.ext)
        call.save()


    for rem in r.scan_iter(match='*remove-%s*' % id):
        c=r.hgetall(rem)
        dt = formattime(c.get('timestamp'))
        ts = paris.localize(dt)
        call.end = ts
        call.save()
        if delete ==True:
            print( "removing : %s" % rem)
            r.delete(rem)
        


print ("Catching Up")
getAddedCalls(False)
for call in Call.objects.filter(end=None):
    getCallsInfo(call, False)

for call in Call.objects.exclude(end=None):
    getCallsInfo(call, True)

            
    
while True:
    getAddedCalls(True)
    for call in Call.objects.filter(end=None):
        getCallsInfo(call, True)

    time.sleep(0.01)
        
    
