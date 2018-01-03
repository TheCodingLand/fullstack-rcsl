import redis
import json

pub = redis.StrictRedis(host="redis", port=6379, db=3)
dataconn = redis.StrictRedis(host="redis", port=6379, db=4)
from graphqlendpoint.models import Agent, Event, Call, Transfer

class Redis(object):
    def __ini__(self):
        pass
    def update(self, item, id , data):
        #notify server that the data has been updated for the frontend

        pub.publish('agent', id)
        #push new state data to redis for frontend subscription
        d = { 'id': id, 'text' : '%s' % data }
        js = json.dumps(d)
        dataconn.lpush('agent', js)
        
            
            
            
        
        
     #          if item == "agent":
   #         try:
    #            agent=Agent.objects.get(ext=id)[0]
    #            data = { 'id': randint(0,1000), 'text' : '%s' % agent.ext, 'timestamp':'31/12/2017' }
    #            data= json.dumps(data)
   #             dataconn.lpush(item, data)
   #         except:
   #             return True
                
            
   #     if item == "call":
    #        Call.objects.get(id=id)
   #         data = { 'action' : 'setcaller', 'timestamp' : "%s" % self.timestamp, 'id' : self.id, 'data' : phone }
    #        dataconn.lpush(item, data)