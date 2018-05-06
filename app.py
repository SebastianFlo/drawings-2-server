from flask import Flask
from flask import jsonify
from flask_restful import Api
from flask_jwt import JWT

# from datetime import timedelta

# database is created based on this
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'  # this should be a secret
api = Api(app)


# Creating database
@app.before_first_request
def create_tables():
    db.create_all()


# authentication endpoint
app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)
# this creates /auth (username, password)
# returns a JWT
# we use that for subsequent requests

# token expiration time
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# authentication key name
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


port = 5000

api.add_resource(Item, '/items/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(Stores, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=port, debug=True)
