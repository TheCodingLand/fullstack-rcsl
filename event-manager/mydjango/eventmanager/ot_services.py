
import json

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mydjango.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()
import requests


CENTRALE = ["571", "572", "573"]

from django.db import connection

class ot_services(object):
  

    def __init__(self):
        print("creating Event")
        
    
            
            ##print(data)
                
    
        #call = Call.objects.update_or_create(ucid=id)[0]
        return True
        
