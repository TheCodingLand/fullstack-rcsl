import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mydjango.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()

from graphqlendpoint.models import Agent, Agent_ot, Agent_unify,Event_ot, Call, Transfer

from django.db import connection

class django_calls_services(object):

    def __init__(self):
        #there are exceptions where databasae connexion is closed when idle for a long time.
        connection.close()
      
    
    def create_call(self, id, timestamp):
        call = Call.objects.update_or_create(ucid=id)[0]
        call.start=timestamp
        call.save()
        print ("create call in django")
        return True
    
    def update_details(self, id, timestamp, data):
        call = Call.objects.update_or_create(ucid=id)[0]
        call.call_type=data
        call.save()
        print ("set details django")
        return True
    
    def transfer_call(self, id, timestamp, data):
        call = Call.objects.update_or_create(ucid=id)[0]
        transfers =call.getTransfers().filter(timestamp=timestamp, destination = data)
        #check if this exists already
        if len(transfers)>0:
            return True
        else:
            call = Call.objects.update_or_create(ucid=id)[0]
            if call.destination == "":
                origin=""
            else:
                origin = call.destination
                
            t = Transfer(call=call, origin=origin, destination = data, timestamp = timestamp)
            t.save()
            
            call.updatehistory()
            call.destination = data
            call.save()
    
        print ("transfer call in django")
        return True
        
    def end(self, id, timestamp):
        call = Call.objects.update_or_create(ucid=id)[0]
        call.end=timestamp
        call.save()
        print ("end call in django")
        return True
    
    def update_agent(self):
        print ("update agent in django")
        return True
    

class django_agents_services(object):
    
    def __init__(self, key):
        self.agent = Agent_unify.objects.update_or_create(ucid=key.id)[0]
        