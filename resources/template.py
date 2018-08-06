from flask_restful import reqparse
from flask_restful import Resource
from models.template import TemplateModel

_template_parser = reqparse.RequestParser()


class Template(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('assets')
    parser.add_argument('css')
    parser.add_argument('styles')
    parser.add_argument('html')
    parser.add_argument('components')

    @classmethod
    def get(cls, template_id):
        template = TemplateModel.find_by_id(template_id)
        if not template:
            return {'message': 'Template not found'}, 404
        return template.json()

    @classmethod
    def post(cls, template_id):
        data = Template.parser.parse_args()

        template = TemplateModel.find_by_id(template_id)

        if template is None:
            template = TemplateModel(**data)
        else:
            template.assets = data['assets']
            template.css = data['css']
            template.styles = data['styles']
            template.html = data['html']
            template.components = data['components']

        template.save_to_db()

        return template.json(), 201

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
