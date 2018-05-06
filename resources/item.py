from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="price cannot be missing")

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="store_id cannot be missing")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):

        if ItemModel.find_by_name(name):
            return {
                'error': 'Item with that name `{}` already exists'.format(name)
            }, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        item.save_to_db()

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = 'DELETE FROM items WHERE name=?'
        # cursor.execute(query, (name, ))

        # connection.commit()
        # connection.close()

        return {'message': '{} Item Deleted'.format(name)}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json(), 201


class Items(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = 'SELECT * FROM items'
        # result = cursor.execute(query)

        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})

        # connection.close()
        # list(map(lambda x: x.json(), ItemMode.query.all())
        items = [item.json() for item in ItemModel.query.all()]
        return {'items': items}, 200
