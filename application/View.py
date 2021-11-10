from flask import Flask
from flask_restful import Resource, Api, request
from flask_cors import CORS

# Local application imports
from .loginInterface import LoginAPI
from .signupInterface import SignupAPI
from .defineMatchInterface import DefineMatchAPI
from .addStadiumInterface import AddStadiumAPI
from .defineSeatsInterface import DedineSeatAPI

app = Flask(__name__)
cors = CORS(app, resources=['/login','/signup','define_match','/add_stadium','/define_seat'])
app.config['CORS_HEADERS'] = '*'
api = Api(app)

api.add_resource(LoginAPI, '/login')
api.add_resource(SignupAPI,'/signup')
api.add_resource(DefineMatchAPI,'/define_match')
api.add_resource(AddStadiumAPI,'/add_stadium')
api.add_resource(DedineSeatAPI,'/define_seat')
@app.after_request
def after_request(response):
    #response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept,Content>
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response