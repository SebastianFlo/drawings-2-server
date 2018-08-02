from flask_restful import reqparse
from flask_restful import Resource
from models.template import TemplateModel

_template_parser = reqparse.RequestParser()


class Template(Resource):

    @classmethod
    def get(cls, template_id):
        template = TemplateModel.find_by_id(template_id)
        if not template:
            return {'message': 'Template not found'}, 404
        return template.json()

    @classmethod
    def delete(cls, template_id):
        template = TemplateModel.find_by_id(template_id)
        if not template:
            return {'message': 'Template not found'}, 404
        template.delete_from_db()
        return {'message': 'Template: {} deleted'.format(template_id)}


class Templates(Resource):

    def get(self):
        templates = [template.json() for template in TemplateModel.find_all()]

        return {'templates': templates}, 200
