from db import db
from models.brand import BrandModel


class ModelModel(db.Model):
    __tablename__ ='models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    id_brand = db.Column(db.Integer, db.ForeignKey("brands.id"))
    brand = db.relationship("BrandModel")

    def json(self):
        return{
            "id": self.id,  
            "name": self.name, 
            "id_brand": self.id_brand
            }

    @classmethod
    def full_json(cls, model):
        return{
            "id": model[0],  # id of the model
            "brand": model[1],  # brand name
            "name": model[2] # name of the model
            }

    # returning only id and name, since there is no need for brand name
    def json_for_brand(self):
        return{
            "id": self.id,  # id of the model
            "name": self.name  # name of the model
            }
                                           
    def __init__(self, name, id_brand):
        self.name = name
        self.id_brand = id_brand
    
    @classmethod
    def find_by_name(cls, name):
        return db.session.query(cls).filter(cls.name == name).first()

    @classmethod
    def find_by_id(cls, _id):
        return db.session.query(cls).filter(cls.id == _id).first()

    @classmethod
    def find_by_part_of_name(cls, name):
        name = name+"%"
        return db.session.query(cls.id, BrandModel.name, cls.name) \
                 .join(BrandModel, isouter=True) \
                 .filter(cls.name.like(name)).all()

    @classmethod
    def find_all(cls):
        return db.session.query(cls.id, BrandModel.name, cls.name) \
                 .join(BrandModel, isouter=True).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    