from flask_restful import Resource, reqparse
from models.model import ModelModel
import json


class Model(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Name is a mandatory field.")
    parser.add_argument('id_brand',
                        type=int,
                        required=True,
                        help="Brand id is a mandatory field.")

    def get(self):
        data = Model.parser.parse_args()
        if ModelModel.find_by_name(data['name'].lower()):
            result = ModelModel.find_by_name(data['name'].lower())
            return {
                    "brand": result[1],
                    "model": result[0].json()
                  }
                          # model=result[0].name)
       # if ModelModel.find_by_part_of_name(data['name'].lower()):
       #      return {
       #             "brands": [
       #                 brand.json() for brand in
       #                 BrandModel.find_by_part_of_name(data['name'].lower())
       #             ]
       #            }
        return {"message": "No result for search '{}' "
                           "in the database.".format(data['name'])}, 401

    def post(self):
        data = Model.parser.parse_args()

        model = ModelModel(data['name'], data['id_brand'])
        model.save_to_db()
        #if ModelModel.find_by_name(data['name'].lower()):
        #    return {"message": "Brand with name '{}' "
        #                       "already exists in the database."
        #                       .format(data['name'])}, 401
        #brand = BrandModel(data['name'].lower())
        brand.save_to_db()
        return brand.json()


class ModelList(Resource):

    def get(self):
        return {"models": [model.json() for model in ModelModel.find_all()]}