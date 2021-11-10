from flask import Flask
from flask_restful import Resource, Api, request
from flask_cors import CORS

# Local application imports
from .loginInterface import LoginAPI
from .signupInterface import SignupAPI


app = Flask(__name__)
cors = CORS(app, resources=['/login','/signup'])
app.config['CORS_HEADERS'] = '*'
api = Api(app)

api.add_resource(LoginAPI, '/login')
api.add_resource(SignupAPI,'/signup')


@app.after_request
def after_request(response):
    #response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept,Content>
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response