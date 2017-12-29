import pytz

from eventmanager.ot_services import ot_services
from eventmanager.django_services import django_calls_services

from datetime import datetime
#from . import frontend_services
paris=pytz.timezone('Europe/Paris')



class Services(object):
    """class that determines which what to do with which redis key"""
    def __init__(self, redishash):
        self.redishash=redishash
        datestr = self.redishash.get('timestamp')
        self.id = redishash.get('id')
        self.action = redishash.get('action')
        
        self.data = ""
        if redishash.get('data'):
            self.data = redishash.get('data')
        try:
            dt = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S.%f')
        except:
            dt = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        
        self.timestamp = paris.localize(dt)
        
        if self.action == "add":
            self.done = self.onCallCreate()
        
        if self.action == "transfer":
            self.done = self.onCallTransfer()
            
        if self.action == "setdetails":
            self.done = self.onCallDetails()
            
        if self.action == "setcaller":
            self.done = self.onCallerUpdated()
            
        if self.action == "changestate":
            self.done = self.onAgentChangeState()
            
        if self.action == "remove":
            self.done = self.onCallFinished()
    
    def onCallCreate(self):
        django = django_calls_services().create_call(self.id, self.timestamp)
        ot = ot_services().create_call(self.id, self.timestamp)
        frontend=True
        return django and ot and frontend
        
    def onCallTransfer(self):
        django = django_calls_services().transfer_call(self.id, self.timestamp,self.data)
        #ot = ot_services.create_or_update(id)
        ot = True
        frontend=True
        return django and ot and frontend
    
    def onCallDetails(self):
        django = django_calls_services().update_details(self.id, self.timestamp, self.data)
        #ot = ot_services.update_details(id)        
        ot=True
        frontend=True
        return django and ot and frontend

    def onCallerUpdated(self):
        django = django_calls_services().update_caller(self.id, self.timestamp, self.data)
        #ot = ot_services.update_details(id)        
        ot=True
        frontend=True
        return django and ot and frontend

    def onCallFinished(self):
        django= django_calls_services().end(self.id, self.timestamp)
        #ot=ot_services.end(id)
        ot=True
        frontend=True
        return django and ot and frontend
        
    def onAgentChangeState(self):
        django = django_agents_services().update_agent(self.id, self.timestamp, self.data)
        ot=True
        frontend=True
        return django and ot and frontend
        
        
        