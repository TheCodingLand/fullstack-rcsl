import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mydjango.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()

from graphqlendpoint.models import Agent, Agent_ot, Agent_unify,Event_ot, Call



class django_calls_services(object):

    def __init__(self, key):
        self.call = Call.objects.update_or_create(ucid=key.id)[0]
        self.key = key
        
    def create_call(self):
        call = Call.objects.update_or_create(ucid=key.id)[0]
        call.start=ts
        call.save()
        print ("create call in django")
        return True
    
    def update_details(self):
        print ("set details django")
        return True
    
    def transfer_call(self):
        
        transfers =call.getTransfer().filter(timestamp=self.key.timestamp, destination = self.key.data)
        if transfers

                    
        for t in transfers:

    
        print ("transfer call in django")
        return True
        
    def end(self):
        print ("end call in django")
        return True
    
    def update_agent(self):
        print ("update agent in django")
        return True
    

class django_agents_services(object):
    
    def __init__(self, key):
        self.agent = Agent_unify.objects.update_or_create(ucid=key.id)[0]
        