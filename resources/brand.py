from flask_restful import Resource, reqparse
from models.brand import BrandModel
from models.vehicletype import VehicleTypeModel

class Brand(Resource):

    # enables finding by the part of the name
    def get(self, name):
        if BrandModel.find_by_part_of_name(name.lower()):
            return {
                    "brands": [
                        brand.json() for brand in
                        BrandModel.find_by_part_of_name(name.lower())
                    ]
                   }
        return {"message": "no result for search '{}' "
                           "in the database".format(name)}, 401

    def post(self, name):
        if BrandModel.find_by_name(name.lower()):
            return {"message": "brand with name '{}' "
                               "already exists in the database"
                               .format(name)}, 401
        parser = reqparse.RequestParser()
        parser.add_argument("id_vehicle_type",
                            type=int,
                            required=True,
                            help="id_vehicle_type is a mandatory field")
        data = parser.parse_args()
        if not VehicleTypeModel.find_by_id(data["id_vehicle_type"]):
            return {"message": "vehicle type with id '{}' "
                               "does not exist in the database"
                               .format(data["id_vehicle_type"])}, 401
        brand = BrandModel(name.lower(), data["id_vehicle_type"])
        brand.save_to_db()
        return brand.json()

    def delete(self, name):
        brand = BrandModel.find_by_name(name.lower())
        if brand:
            brand.delete_from_db()
            return {"message": "Brand with name '{}' "
                               "has been deleted."
                               .format(name)}, 200
        return {"message": "Brand with name '{}' "
                           "does not exist in the database"
                           .format(name)}, 401

    def put(self, name):
        if BrandModel.find_by_name(name.lower()):
            return {"message": "Brand with name '{}' "
                               "already exists in the database."
                               .format(name)}, 401
        parser = reqparse.RequestParser()
        parser.add_argument('id',
                            type=int,
                            required=True,
                            help="Id is a mandatory field.")
        data = parser.parse_args()
        if BrandModel.find_by_id(data['id']):
            brand = BrandModel.find_by_id(data['id'])
            old_name = brand.name
            brand.name = name.lower()
            brand.save_to_db()
            return {"message": "Brand name has been updated "
                               "from '{}' to '{}'."
                               .format(old_name, name)}, 200
        return {"message": "Brand with id '{}' "
                           "does not exist in the database."
                           .format(data['id'])}, 401


class BrandList(Resource):

    def get(self):
        return {"brands": [BrandModel.full_json(brand) for brand in BrandModel.find_all()]}




