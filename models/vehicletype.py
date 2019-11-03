from db import db


class VehicleTypeModel(db.Model):
    __tablename__='vehicletypes'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_type = db.Column(db.String(25))
    brands = db.relationship("BrandModel",
                              lazy="dynamic",
                              cascade="all,delete",
                              backref="parent")


    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type

    def json(self):
        return {
            'id': self.id,
            'vehicle_type': self.vehicle_type,
            'brands': [brand.json_for_vehicle_type() for brand in self.brands.all()]
        }

    @classmethod
    def find_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def find_by_name(cls, name):
        return db.session.query(cls).filter(cls.vehicle_type == name).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return db.session.query(cls).filter(cls.id == _id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


