import pytz

from eventmanager import ot_services
from eventmanager.django_services import django_calls_services


#from . import frontend_services
paris=pytz.timezone('Europe/Paris')



class Services(object):
    """class that determines which what to do with which redis key"""
    def __init__(self, redishash):
        self.redishash=redishash
        datestr = self.redishash.get('timestamp')
        self.id = redishash.get('id')
        self.action = redishhash.get('action')
        
        self.data = ""
        if rediskey.get('data'):
            self.data = redishash.get('data')
        try:
            dt = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S.%f')
        except:
            dt = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        
        self.timestamp = paris.localize(dt)
        
        if action == "add":
            self.done = self.onCallCreated()
        
        if action == "transfer":
            self.done = self.onTransfer()
            
        if action == "setdetails":
            self.done = self.onCallDetails()
            
        if action == "setcaller":
            self.done = self.onCallerUpdated()
            
        if action == "changestate":
            self.done = self.onAgentChangeState()
            
        if action == "remove":
            self.done = self.onCallFinished()
    
    def onCallCreated(self):
        django = django_calls_services.create_call(self)
        ot = True
        frontend=True
        return django and ot and frontend
        
    def onCallTransfer(self):
        django = django_calls_services.transfer_call(self)
        ot = ot_services.create_or_update()
        frontend = True
        frontend=True
        return django and ot and frontend
    
    def onCallDetails(self):
        django = django_calls_services.update_details(self)
        ot = ot_services.update_details_if_helpdesk(self)        
        frontend=True
        return django and ot and frontend

    def onCallerUpdated(self):
        django = django_calls_services.update_details_call(self)
        ot = ot_services.update_details(self)        
        frontend=True
        return django and ot and frontend

    def onCallFinished(self):
        django= django_calls_services.end(self)
        ot=ot_services.end(self)
        frontend=True
        return django and ot and frontend
        
    def onAgentChangeState(self):
        django = django_agents_services.update_agent()
        ot=True
        frontend=True
        return django and ot and frontend
        
        
        