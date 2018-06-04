from flask_restful import Resource
from models.category import CategoryModel


class Category(Resource):
    def get(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            return category.json()
        return {'message': 'Category not found'}, 404

    def post(self, name):
        if CategoryModel.find_by_name(name):
            return {'message': 'Category already exists'}, 400
        category = CategoryModel(name)

        try:
            category.save_to_db()
        except Exception:
            return {'message': 'Error occured while creating category'}, 500

        return category.json(), 201

    def delete(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            category.delete_from_db()

        return {'message': 'Category Deleted'}, 200


class Categories(Resource):
    def get(self):
        return {'categories': [category.json() for category in CategoryModel.find_all()]}, 200
