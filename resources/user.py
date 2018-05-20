from flask_restful import reqparse
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    jwt_required,
    get_raw_jwt,
    get_jwt_identity
)
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be missing")
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be missing")


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {
                'user': None,
                'message': 'A user with that username already exists'
            }, 400

        user = UserModel(**data)
        user.save_to_db()

        return {
            'user': data['username'],
            'message': 'User created successfully'
        }, 201


class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User: {} deleted'.format(user_id)}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user
        user = UserModel.find_by_username(data['username'])

        # check passwork
        if user and safe_str_cmp(user.password, data['password']):
            # create access token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # jwt ID , unique ID for jwt
        BLACKLIST.add(jti)
        return {'message': 'Succesfully logged out'}, 200

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {
            'access_token': new_token
        }, 200