import graphene

from AwesomeStore.models import Category, Products

class Agent(graphene.ObjectType):
    ext = graphene.String(description='Agent Phone Extention')
    phone_login = graphene.String(description='Agent Login for phone system')
    ticket_system_login = graphene.String(description='Agent Login for phone system')
    
    current_call= graphene.String(description='Agent Login for phone system')
    state = str()
    loggedin=Bool()
    
    def login(self):
        
        
    
    ...
    
    def serialize(self):
        return {
            'Title': self.Title, 
            'Description': self.Description,
        }

