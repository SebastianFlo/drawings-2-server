from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    size = db.Column(db.String(80))
    description = db.Column(db.String(500))
    url = db.Column(db.String(2000))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('CategoryModel')

    def __init__(self, name, price, size, description, url, category_id):
        self.name = name
        self.price = price
        self.size = size
        self.description = description
        self.url = url
        self.category_id = category_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'size': self.size,
            'description': self.description,
            'url': self.url,
            'category_id': self.category_id,
            'price': self.price
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
