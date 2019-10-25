from flask_restful import Resource, reqparse
from models.brand import BrandModel


class Brand(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Name is a mandatory field.")

    # enables finding by the part of the name
    def get(self):
        data = Brand.parser.parse_args()
        if BrandModel.find_by_part_of_name(data['name'].lower()):       
            return {
                    "brands": [
                        brand.json() for brand in
                        BrandModel.find_by_part_of_name(data['name'].lower())
                    ]
                   }
        return {"message": "No result for search '{}' "
                           "in the database.".format(data['name'])}, 401

    def post(self):
        data = Brand.parser.parse_args()
        if BrandModel.find_by_name(data['name'].lower()):
            return {"message": "Brand with name '{}' "
                               "already exists in the database."
                               .format(data['name'])}, 401
        brand = BrandModel(data['name'].lower())
        brand.save_to_db()
        return brand.json()

    def delete(self):
        data = Brand.parser.parse_args()
        brand = BrandModel.find_by_name(data['name'].lower())
        if brand:
            brand.delete_from_db()
            return {"message": "Brand with name '{}' "
                               "has been deleted."
                               .format(data['name'])}, 200
        return {"message": "Brand with name '{}' "
                           "does not exist in the database"
                           .format(data['name'])}, 401


class BrandList(Resource):

    def get(self):
        return {"brands": [brand.json() for brand in BrandModel.find_all()]}


class BrandUpdate(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int,
                        required=True,
                        help="Id is a mandatory field")
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Name is a mandatory field")

    # updates brand name as per given id
    def put(self):
        data = BrandUpdate.parser.parse_args()
        if BrandModel.find_by_id(data['id']):
            brand = BrandModel.find_by_id(data['id'])
            old_name = brand.name
            brand.name = data['name']
            brand.save_to_db()
            return {"message": "Brand name has been updated "
                               "from '{}' to '{}'."
                               .format(old_name, data['name'])}, 200
        return {"message": "Brand with id '{}' "
                           "does not exist in the database"
                           .format(data['id'])}, 401
