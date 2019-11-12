from flask_restful import Resource, reqparse
from models.model import ModelModel
from models.brand import BrandModel
from sqlalchemy import exc


class Model(Resource):

    parser = reqparse.RequestParser()

    def get(self, name):
       if ModelModel.find_by_part_of_name(name.lower()):
           return {
                  "models":
                  [ModelModel.full_json(model) for model in
                  ModelModel.find_by_part_of_name(name.lower())]
               }, 200
       return {"message": "No result for search '{}' "
                          "in the database.".format(name)}, 401

    @admin_required
    def post(self, name):
        Model.parser.add_argument("id_brand",
                                  type=int,
                                  required=True,
                                  help="id_brand is a mandatory field")
        data = Model.parser.parse_args()
        try:        
            model = ModelModel(name, data["id_brand"])                       
            model.save_to_db()
        except exc.IntegrityError as e: # integrity errors from mysql
            return {"message": "{}".format(e.orig.args[1])}, 401
        return model.json()

    @admin_required
    def delete(self,name):
        model = ModelModel.find_by_name(name.lower())
        if model:
            model.delete_from_db()
            return {"message": "Model with name '{}' "
                               "has been deleted."
                               .format(name)}, 200
        return {"message": "Model with name '{}' "
                           "does not exist in the database"
                           .format(name)}, 401

    @admin_required
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('id',
                            type=int,
                            required=True,
                            help="Id is a mandatory field.")
        data = parser.parse_args()
        if ModelModel.find_by_id(data['id']):
            model = ModelModel.find_by_id(data['id'])
            old_name = model.name
            model.name = name.lower()
            model.save_to_db()
            return {"message": "Model name has been updated "
                               "from '{}' to '{}'."
                               .format(old_name, name)}, 200
        return {"message": "Model with id '{}' "
                           "does not exist in the database."
                           .format(data['id'])}, 401


class ModelList(Resource):

    def get(self):
        return {"models":
                [ModelModel.full_json(model) for model in ModelModel.find_all()]}
