from flask_restful import Resource, reqparse
from models.vehicletype import VehicleTypeModel


class VehicleType(Resource):
    
    def post(self,name):
        if VehicleTypeModel.find_by_name(name.lower()):
            return {
                    "message":"Vehicle type with name '{}'"
                              "already exists in the database."
                              .format(name)
                   },401
        vehicle_type = VehicleTypeModel(name.lower())
        vehicle_type.save_to_db()
        return vehicle_type.json()

    def delete(self,name):
        vehicle_type = VehicleTypeModel.find_by_name(name.lower())
        if vehicle_type:
            vehicle_type.delete_from_db()
            return {"message": "Vehicle type with name '{}' "
                               "has been deleted."
                               .format(name)}, 200
        return {"message": "Vehicle type with name '{}' "
                           "does not exist in the database"
                           .format(name)}, 401

    def put(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument("id",
                            type=int,
                            required=True,
                            help="id is a mandatory field")
        data = parser.parse_args()
        if VehicleTypeModel.find_by_id(data["id"]):
            vehicle_type = VehicleTypeModel.find_by_id(data["id"])
            old_name = vehicle_type.vehicle_type
            vehicle_type.vehicle_type = name.lower()
            vehicle_type.save_to_db()
            return {"message": "Vehicle type name has been updated "
                               "from '{}' to '{}'."
                               .format(old_name, name)}, 200
        return {"message": "Vehicle type with id '{}' "
                           "does not exist in the database."
                           .format(data["id"])}, 401



class VehicleTypeList(Resource):

    def get(self):
        return {"vehicle_types": [vehicle_type.json() for vehicle_type in VehicleTypeModel.find_all()]}
