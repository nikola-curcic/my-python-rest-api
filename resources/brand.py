from flask_restful import Resource, reqparse
from models.brand import BrandModel


class Brand(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Name is a mandatory field")

    def get(self):
        data = Brand.parser.parse_args()
        brand = BrandModel.find_by_name(data['name'].lower())
        print(brand)

    def post(self):
        data = Brand.parser.parse_args()
        brand = BrandModel.find_by_name(data['name'].lower())
        print(brand)
        if brand:
            return {"message": "Brand with this name already exists"}, 401
        brand = BrandModel(data['name'].lower())
        brand.save_to_db()
        return brand.json()

    def delete(self):
        data = Brand.parser.parse_args()
        brand = BrandModel.find_by_name(data['name'].lower())
        if brand:
            brand.delete_from_db()
            return {"message": "Brand with this name has been deleted"}, 200
        return {"message": "Brand with this name does not exist in the data base"}, 200


class BrandList(Resource):

    def get(self):
        return {"brands": [brand.json() for brand in BrandModel.find_all()]}
