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

class DedineSeatAPI(Resource):
    def post(self):
        if not input_validator(request):
            logger.error("Input is not in JSON format.\t" + str(request.data))
            flask.abort(400, "The input must be in JSON format.")
        raw_data = request.data
        input_data = json.loads(raw_data)
        my_database = database()
        if not my_database.db_error:
            try:
                stadium_id = input_data['stadium_id']
                number_of_seat = input_data['number_of_seat']
                match_id = input_data['match_id']
            except KeyError:
                logger.error("Input is not in JSON format.\t" + str(request.data))
                flask.abort(400, "All The Json's Parameter Not Satisfied")
            else:
                result,msg = my_database.defineSeat(stadium_id=stadium_id,number_of_seat=number_of_seat,match_id=match_id)
                if result:
                    output = {
                        'response': 'Seats successfully Created!',
                        'status': 200,
                        'errors': []
                    }
                else:
                    output = {
                        'response': [],
                        'status': 300,
                        'errors': [f'{msg} :(']
                    }
            my_database.connectionClose()
        else:
            output = {
                'response': None,
                'status': 300,
                'errors': ["database not connected"]
            }
        return output
