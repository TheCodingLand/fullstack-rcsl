import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mydjango.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()

from graphqlendpoint.models import Agent, Event, Call, Transfer

from django.db import connection





class django_calls_services(object):

    def __init__(self):
        #there are exceptions where databasae connexion is closed when idle for a long time.
        connection.close()
      

    def create_call(self, id, timestamp):
        call = Call.objects.update_or_create(ucid=id)[0]
        call.start=timestamp
        call.save()
        return True
    
    def set_caller(self, id, timestamp, data):
        call = Call.objects.update_or_create(ucid=id)[0]
        call.origin=data
        call.save()

        return True
    
    def update_details(self, id, timestamp, data):
        call = Call.objects.update_or_create(ucid=id)[0]
        call.call_type=data
        call.save()

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
            
            if origin !=data:
                t = Transfer(call=call, origin=origin, destination = data, timestamp = timestamp)
                t.save()
            call.updatehistory()
            try:
                agent=Agent.objects.get(ext=data)[0]
                if agent.user in Groups.objects.get('name=helpdesk')
                    call.primaryagent = Agent
                    call.save()
                
            except:
                log.info('not an agent %s' % data )
            call.destination = data
            call.save()
        return True
        
    def end(self, id, timestamp):
        call = Call.objects.update_or_create(ucid=id)[0]
        call.end=timestamp
        call.save()
        return True
    
    def update_agent(self):

        return True


class django_agents_services(object):
    
    def __init__(self):
        connection.close()
    def update_agent(self, key):
        self.agent = Agent.objects.update_or_create(phone_login=key.id)[0]
        self.agent.phone_state=key.data
        self.agent.save()
        
        
        