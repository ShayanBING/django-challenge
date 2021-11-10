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

class SignupAPI(Resource):
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
                password = input_data['password']
                first_name = input_data['first_name']
                last_name = input_data['last_name']
                email = input_data['email']
                mobile = input_data['mobile']
            except KeyError:
                logger.error("Input is not in JSON format.\t" + str(request.data))
                flask.abort(400, "All The Json's Parameter Not Satisfied")
            else:
                result = my_database.signUp(user_name=user_name, password=password,first_name=first_name,last_name=last_name,email=email,mobile=mobile)
                if result:
                    output = {
                        'response': 'signup successfully!',
                        'status': 200,
                        'errors': []
                    }
                else:
                    output = {
                        'response': [],
                        'status': 300,
                        'errors': ['User_name already Taken! :(']
                    }
            my_database.connectionClose()
        else:
            output = {
                'response': None,
                'status': 300,
                'errors': ["database not connected"]
            }
        return output
