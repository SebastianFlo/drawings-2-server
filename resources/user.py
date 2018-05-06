from flask_restful import reqparse
from flask_restful import Resource

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be missing")
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be missing")

    def post(self):
        data = UserRegister.parser.parse_args()

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
