from db import db


class TemplateModel(db.Model):
    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True)
    assets = db.Column(db.String())
    css = db.Column(db.String())
    styles = db.Column(db.String())
    html = db.Column(db.String())
    components = db.Column(db.String())

    def __init__(self, id, assets, css, styles, html, components):
        self.assets = assets
        self.css = css
        self.styles = styles
        self.html = html
        self.components = components

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            # 'id': self.id,
            'assets': self.assets,
            'css': self.css,
            'styles': self.styles,
            'html': self.html,
            'components': self.components
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
