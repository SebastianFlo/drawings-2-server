from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    fresh_jwt_required
)
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=False)
    parser.add_argument('size',
        required=False)
    parser.add_argument('description',
        required=False)
    parser.add_argument('url',
        required=True,
        help="url cannot be missing")
    parser.add_argument('category_id',
        type=int,
        required=True,
        help="category_id cannot be missing")

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    @fresh_jwt_required
    def post(self, name):

        if ItemModel.find_by_name(name):
            return {
                'error': 'Item with that name `{}` already exists'.format(name)
            }, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        item.save_to_db()

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        # use claims here
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin priviledge required'}, 401

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': '{} Item Deleted'.format(name)}

    @jwt_required
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.size = data['size']
            item.description = data['description']
            item.url = data['url']
            item.category_id = data['category_id']

        item.save_to_db()

        return item.json(), 201


class Items(Resource):

    def get(self):
        items = [item.json() for item in ItemModel.find_all()]

        return {'items': items}, 200
