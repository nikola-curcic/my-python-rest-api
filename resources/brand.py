from flask_restful import Resource, reqparse
from models.brand import BrandModel
from models.vehicletype import VehicleTypeModel
from sqlalchemy import exc

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

    @admin_required
    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("id_vehicle_type",
                            type=int,
                            required=True,
                            help="id_vehicle_type is a mandatory field")
        data = parser.parse_args()
        try:        
            brand = BrandModel(name, data["id_vehicle_type"])                       
            brand.save_to_db()
        except exc.IntegrityError as e: # integrity errors from mysql
            return {"message": "{}".format(e.orig.args[1])}, 401
        return brand.json()

    @admin_required
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

    @admin_required
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




