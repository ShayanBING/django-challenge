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

class AddStadiumAPI(Resource):
    def post(self):
        if not input_validator(request):
            logger.error("Input is not in JSON format.\t" + str(request.data))
            flask.abort(400, "The input must be in JSON format.")
        raw_data = request.data
        input_data = json.loads(raw_data)
        my_database = database()
        if not my_database.db_error:
            try:
                id = input_data['id']
                name = input_data['name']
                seats_num = input_data['seats_num']
                home_team_id = input_data['home_team_id']
            except KeyError:
                logger.error("Input is not in JSON format.\t" + str(request.data))
                flask.abort(400, "All The Json's Parameter Not Satisfied")
            else:
                result = my_database.addStadium(id=id,name=name,seats_num=seats_num,home_team_id=home_team_id)
                if result:
                    output = {
                        'response': 'Stadium successfully Created!',
                        'status': 200,
                        'errors': []
                    }
                else:
                    output = {
                        'response': [],
                        'status': 300,
                        'errors': ['Stadium already added! :(']
                    }
            my_database.connectionClose()
        else:
            output = {
                'response': None,
                'status': 300,
                'errors': ["database not connected"]
            }
        return output
