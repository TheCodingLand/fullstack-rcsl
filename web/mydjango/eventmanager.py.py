import redis

centrale = ['571', '572', '573']
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mydjango.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()

from graphqlendpoint.models import Agent, Agent_ot, Agent_unify,Event_ot, Call

while True:

    r = redis.StrictRedis(host='redis', port=6379, db=0)
    for key in r.scan_iter('*'):
        # delete the key
        
        try:
            value = r.hgetall(key)
            print(value.get(b'id'))
        except:
            pass
        
        #for key, v in value:
        #    output[key.decode(self.encoding)] = v.decode(self.encoding)
        #print (output)
      
