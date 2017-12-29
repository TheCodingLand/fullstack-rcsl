import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mydjango.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()

from graphqlendpoint.models import Agent, Agent_ot, Agent_unify,Event_ot, Call

def create_or_update(key):
    
    print("check if helpdesk")
    print("create event")
    print("return ID, store in django")
    
def update(key):
    print("update if event id in django")
    
def end(key):
    print("update if event id in django")
    
def update_details(self):
    print("updateing details ot")