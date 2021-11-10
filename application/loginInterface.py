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

class LoginAPI(Resource):
    def get(self):
        if not input_validator(request):
            logger.error("Input is not in JSON format.\t" + str(request.data))
            flask.abort(400, "The input must be in JSON format.")
        raw_data = request.data
        input_data = json.loads(raw_data)
        my_database = database()
        if not my_database.db_error:
            user_name = input_data['user_name']
            password = input_data['password']
            msg , result = my_database.login(user_name=user_name,password=password)
            if result:
                output = {
                    'response': msg,
                    'status': 200,
                    'errors': []
                }
            else:
                if msg == 'user not found':
                    output ={
                        'response': [],
                        'status': 404,
                        'errors': [msg]
                    }
                else:
                    output ={
                        'response': [],
                        'status': 401,
                        'errors': [msg]
                    }
        else:
            output = {
                'response' : None,
                'status' : 300,
                'errors' : ["database not connected"]
            }
        my_database.connectionClose()
        return output
