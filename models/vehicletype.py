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




