# project/api/views.py
from flask_restplus import Namespace, Resource, fields
from ot_ws.api.models.event import event, ticket

from ot_ws.api.restplus import api
from ot_ws.ot.query_ot import query_ot
from ot_ws.ot.ot_models import Event, Ticket, Category
from ot_ws.ot.serialize import serialize, test
#these hold our data model folder, fields list, required fields
import time
from ot_ws.ot.ot_field import *


ns = api.namespace('ot/events', description='Operations related to OT events')


@ns.route('/schema')
class Swagger(Resource):
    def get(self):
        return api.__schema__


@ns.route('/ping')
class SanityCheck(Resource):
    def get(self):
        print(json.dumps(api.__schema__))
        return {
        'status': 'success',
        'message': 'pong!'
        }



@api.response(404, 'object not found.')
@ns.route('/ot_objects/metadata/<int:object_id>', methods=['GET'])
class ObjectsMetadata(Resource):
    def get(self, object_id):
        """Get single event details"""
        response_object = {
            'status': 'fail',
            'message': 'Event does not exist'
        }
        try:
            e=query_ot()
            e.get(object_id)
            print ("%s" % e.xml_result)
            result=serialize(e.xml_result.decode("utf-8"))
            ot_object=result.metadata
            if not ot_object:
                return response_object, 404
            else:
                response_object = {
                    'status': 'success',
                    'data': ot_object
                }
                return response_object, 200
        except ValueError:
            return response_object, 404


def getFields(object_model, data):
    fields = []
    for key in data.keys():
        if key in object_model.fields.keys():
            cls = globals()[object_model.fields[key]] 
            f = cls(key)
            f.value = data[key]   
            fields.append(f)
        else:
            print ("field not in globals")
            raise ValueError('field not in globals')
    return fields    



event_model=Event()
@api.response(400, 'failed.')
@ns.route('/events')
class EventAdd(Resource):
    @api.response(201, 'Event successfully created.')
    @api.expect(event)
    def put(self):
        time.sleep(1)
        post_data = request.get_json()
        
        #if not post_data:
        #    response_object = {
        #        'status': 'fail',
        #        'message': 'Invalid payload.'
        #    }
        #   return jsonify(response_object), 400
       
        try:
            fields=getFields(event_model,post_data)
        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload parsing fields.'
            }
            return jsonify(response_object), 400
        try:
            r = query_ot()
            print (event_model)
            print(fields)
            event = r.add(event_model,fields)
            if event:
                response_object = {
                    'status': 'success',
                    'message': 'event was added!',
                    'event' : event
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Sorry. failed.'
                }
                return response_object, 400
        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
            return jsonify(response_object), 400

@ns.route('/events/<int:event_id>', methods=['GET'])
class EventItem(Resource):
    def get(self, event_id):
        """Get single event details"""
        response_object = {
            'status': 'fail',
            'message': 'Event does not exist'
        }
        try:
            e=query_ot()
            e.get(event_id)
            result=serialize(e.xml_result.decode("utf-8"))
            event=result.res
            #event = test()
            if not event:
                return response_object, 404
            
            wrong_type=False
            unexpected_fields = []
            for f in event.keys():
                if f not in event_model.fields:
                    unexpected_fields.append(f)
                    wrong_type=True
            if wrong_type == True:
                response_object = {
                'status': 'fail',
                #'message': 'unexpected fields : %s' % (unexpected_fields)
                'message': 'wrong object returned'
                }
                return response_object, 400
            else:
                response_object = {
                    'status': 'success',
                    'data': event
                }
                return response_object, 200
        except ValueError:
            return response_object, 404
    


@ns.route('/events/ucid/<int:event_ucid>', methods=['GET'])
class EventItem(Resource):
    def get(self, event_ucid):
        """Get single event details"""
        response_object = {
            'status': 'fail',
            'message': 'Event does not exist'
        }
        try:
            e=query_ot()
            e.GetEventByUCID(event_ucid)
            result=serialize(e.xml_result.decode("utf-8"))
            event=result.res
            #event = test()
            if not event:
                return response_object, 404
            
            wrong_type=False
            unexpected_fields = []
            for f in event.keys():
                if f not in event_model.fields:
                    unexpected_fields.append(f)
                    wrong_type=True
            if wrong_type == True:
                response_object = {
                'status': 'fail',
                #'message': 'unexpected fields : %s' % (unexpected_fields)
                'message': 'wrong object returned'
                }
                return response_object, 400
            else:
                response_object = {
                    'status': 'success',
                    'data': event
                }
                return response_object, 200
        except ValueError:
            return response_object, 404







ticket_model=Ticket()
  
@ns.route('/tickets/<int:ticket_id>', methods=['GET'])
class TicketItem(Resource):
    def get(self, ticket_id):
        """Get single ticket details"""
        response_object = {
            'status': 'fail',
            'message': 'Event does not exist'
        }
        try:
            t=query_ot()
            t.get(ticket_id)
            result=serialize(t.xml_result.decode("utf-8"))
            ticket=result.res
            #event = test()
            if not ticket:
                return response_object, 404
            
            wrong_type=False
            unexpected_fields = []
            for f in ticket.keys():
                if f not in ticket_model.fields:
                    unexpected_fields.append(f)
                    wrong_type=True
            if wrong_type == True:
                response_object = {
                'status': 'fail',
                'message': 'wrong object returned'
                }
                return response_object, 400
            else:
                response_object = {
                    'status': 'success',
                    'data': ticket
                }
                return response_object,200
        except ValueError:
            return response_object, 404
    

ticket_model=Ticket()
@api.response(400, 'failed.')
@ns.route('/tickets')
class TicketAdd(Resource):
    @api.response(201, 'Event successfully created.')
    @api.expect(ticket)
    def put(self):
        time.sleep(1)
        post_data = request.get_json()
        
        #if not post_data:
        #    response_object = {
        #        'status': 'fail',
        #        'message': 'Invalid payload.'
        #    }
        #   return jsonify(response_object), 400
       
        try:
            fields=getFields(ticket_model,post_data)
        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload parsing fields.'
            }
            return jsonify(response_object), 400
        try:
            r = query_ot()
            print (ticket_model)
            print(fields)
            event = r.add(ticket_model,fields)
            if event:
                response_object = {
                    'status': 'success',
                    'message': 'ticket was added!',
                    'ticket' : ticket
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Sorry. failed.'
                }
                return response_object, 400
        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
            return jsonify(response_object), 400
