from db import db
from models.vehicletype import VehicleTypeModel


class BrandModel(db.Model):
    __tablename__ ='brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    models = db.relationship("ModelModel", 
                             lazy="dynamic",
                             cascade="all,delete", # without dynamic it performs query and returns object
                             backref="parent")     # this way it does not return a result, so all() is necessary
    id_vehicle_type = db.Column(db.Integer, db.ForeignKey("vehicletypes.id"), nullable=False)
    vehicle_type = db.relationship("VehicleTypeModel")
    
    def __init__(self, name, id_vehicle_type):
        self.name = name
        self.id_vehicle_type = id_vehicle_type

    def json(self):
        return {
                'id': self.id,
                'name': self.name,
                'models': [model.json_for_brand() for model in self.models.all()]
            }

    @classmethod
    def full_json(cls, model):
        return{
            "id": model[0],  
            "vehicle_type": model[1],  
            "name": model[2] 
            }
    
    def json_for_vehicle_type(self):
        return {
                'id': self.id,
                'name': self.name
             }
    
    @classmethod
    def find_by_name(cls, name):
        return db.session.query(cls).filter(cls.name == name).first()

    @classmethod
    def find_by_id(cls, _id):
        return db.session.query(cls).filter(cls.id == _id).first()

    @classmethod
    def find_by_part_of_name(cls, name):
        name = name+"%"
        return db.session.query(cls).filter(cls.name.like(name)).all()

    @classmethod
    def find_all(cls):
        return db.session.query(cls.id, VehicleTypeModel.vehicle_type, cls.name) \
                 .join(VehicleTypeModel, isouter=True).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    



