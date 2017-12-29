
#curl -X GET --header 'Accept: application/json' 'http://148.110.107.15:5001/api/ot/events/events/ucid/8091514540134112'
import json

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mydjango.settings')
import django
from django.core.exceptions import ObjectDoesNotExist
django.setup()
import requests


from django.db import connection

class ot_services(object):

    def __init__(self):
        #there are exceptions where databasae connexion is closed when idle for a long time.
        connection.close()
    def create_call(self, id, timestamp):
        #Event_ot = Event_OT()
        url = 'http://ot-ws:5000/api/ot/events/events/ucid/%s'% id
        resp = requests.get(url=url)
        data = json.loads(resp.text)        
        print(data)
        #call = Call.objects.update_or_create(ucid=id)[0]
        return True
    
   