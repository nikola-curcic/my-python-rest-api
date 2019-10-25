from db import db
from models.brand import BrandModel


class ModelModel(db.Model):
    __tablename__ = "models"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    id_brand = db.Column(db.Integer, db.ForeignKey("brands.id"))
    brand = db.relationship("BrandModel")

    def json(self):
        return {
                'id': self.id,
                'name': self.name,
            }

    def __init__(self, name, id_brand):
        self.name = name
        self.id_brand = id_brand
    
    @classmethod
    def find_by_name(cls, name):
      #  return db.session.query(cls).filter(cls.name == name).first()

        return db.session.query(cls, BrandModel.name).join(BrandModel).filter(cls.name == name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return db.session.query(cls).all()