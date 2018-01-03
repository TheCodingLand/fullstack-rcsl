import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mydjango.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()
import json
from graphqlendpoint.models import Agent, Event, Call, Transfer
import requests
from django.db import connection
from eventmanager.redis import Redis
CENTRALE = ["571", "572", "573"]



class django_calls_services(object):

    def __init__(self):
        #there are exceptions where databasae connexion is closed when idle for a long time.
        connection.close()
      

    def create_call(self, id, timestamp):
        call = Call.objects.get_or_create(ucid=id)[0]
        call.start=timestamp
        call.save()
        return True
    
    def set_caller(self, id, timestamp, data):
        call = Call.objects.get_or_create(ucid=id)[0]
        call.origin=data
        call.save()

        return True
    
    def update_details(self, id, timestamp, data):
        call = Call.objects.get_or_create(ucid=id)[0]
        call.call_type=data
        call.save()

        return True
        
    def create_event(self, call):
        print ("getting id")
        url = 'http://ot-ws:5000/api/ot/events/events/ucid/%s' % call.ucid
        #if call.event:
        #    if call.event.ot_id:
        #        url = 'http://ot-ws:5000/api/ot/events/events/%s' % call.event.ot_id
            #Event_ot = Event_OT()
        
        resp = requests.get(url=url)
        ot= json.loads(resp.text)
        #print (ot)
        
        if resp.status_code==404:
            #print ("create event in ot as is doesnt exist")
            event = Event(creationdate = call.start, call=call)
            event.save()
            call.event = event
            call.save()
        elif resp.status_code==200:
            if ot['id'] !=0:
                #print (ot['id'])
                event =Event.objects.get_or_create(ot_id=ot['id'])[0]
                event.save()


            if call.event:
                call.event.ot_id = ot['id']
                call.save()
    
    def transfer_call(self, id, timestamp, data):
        #print("managing a transfer")
        
        call = Call.objects.get_or_create(ucid=id)[0]
        if data in CENTRALE:
            call.isContactCenterCall=True
            call.save()
            self.create_event(call)

        
        transfers = call.getTransfers().filter(timestamp=timestamp, destination = data)
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
                if agent.user in Groups.objects.get('name=helpdesk'):
                    call.primaryagent = agent
                    call.save()
                
            except:
                pass
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
    
    def login(self, id, data):
        self.agent = Agent.objects.get_or_create(phone_login=id)[0]
        self.agent.phone_login = id
        print ("Agent loggin in with %s, ext %s" % (id,data))
        self.agent.active=True
        self.agent.ext = data
        self.agent.save()
        redis= Redis().update('agent', id, data)
        return True
        
    def changeACDstate(self, id, data):
        try:
            self.agent = Agent.objects.get(phone_login=id)
            self.agent.phone_state=data
            self.agent.save()
            
         
        except:
            pass
        redis= Redis().update('agent', id, data)
        return True
        
    def linkcall(self, id, data):
        #print ("linkCall agent : %s, call %s" % (id, data))
        try:
            self.agent = Agent.objects.get(phone_login=id)
            self.call = Call.objects.get(ucid=data)
            self.call.primaryagent=(self.call)
            self.agent.save()
            self.call.save()
           
            return True
        except:
            pass
        redis= Redis().update('agent', id, data)
        return True
            
    
    def changeDeviceState(self, id, data):
        try:   
            self.agent = Agent.objects.get(phone_login=id)
            self.agent.device_state=data
            self.agent.save()
            
        except:
            pass
        redis= Redis().update('agent', id, data)
        return True
     
    def logoff(self, id, data):
        try:
            self.agent = Agent.objects.get(phone_login=id)
            self.agent.active=True
            self.agent.save()
           
        except:
            pass
        redis= Redis().update('agent', id, data)   
        return True
        
    

    