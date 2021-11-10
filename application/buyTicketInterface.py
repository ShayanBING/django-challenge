# Standard library imports
import json

# Third party imports
import flask
from flask_restful import Resource, request
from log_handler.Setup import logger
from application.databaseconnect import database



def input_validator(input_request):
    try:
        text_json = input_request.data
        json_obj = json.loads(text_json)
    except:
        return False
    return True

class BuyTicketAPI(Resource):
    def post(self):
        if not input_validator(request):
            logger.error("Input is not in JSON format.\t" + str(request.data))
            flask.abort(400, "The input must be in JSON format.")
        raw_data = request.data
        input_data = json.loads(raw_data)
        my_database = database()
        if not my_database.db_error:
            try:
                user_name = input_data['user_name']
                seat_num = input_data['seat_num']
                match_id = input_data['match_id']
            except KeyError:
                logger.error("Input is not in JSON format.\t" + str(request.data))
                flask.abort(400, "All The Json's Parameter Not Satisfied")
            else:
                result,msg = my_database.buyTicket(user_name,seat_num,match_id)
                if result:
                    output = {
                        'response': 'Ticket Buy successfully! :D',
                        'status': 200,
                        'errors': []
                    }
                else:
                    if msg == 'not_done':
                        output = {
                            'response': [],
                            'status': 300,
                            'errors': ['Seats already Taken! :(']
                        }
                    else:
                        output = {
                            'response': [],
                            'status': 401,
                            'errors': [msg]
                        }
            my_database.connectionClose()
        else:
            output = {
                'response': None,
                'status': 300,
                'errors': ["database not connected"]
            }
        return output
