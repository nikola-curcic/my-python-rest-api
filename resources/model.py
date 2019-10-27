from flask_restful import Resource, reqparse
from models.model import ModelModel


class Model(Resource):

    parser = reqparse.RequestParser()

    # mora da se doda u listu jer vraca objekat modela + naziv brenda
    def get(self, name):
        if ModelModel.find_by_part_of_name(name.lower()):
            return {
                    "models":
                    [ModelModel.json(model) for model in
                     ModelModel.find_by_part_of_name(name.lower())]
                    }, 200
        return {"message": "No result for search '{}' "
                           "in the database.".format(name)}, 401

    def post(self, name):
        Model.parser.add_argument('id_brand',
                                  type=int,
                                  required=True,
                                  help="id_brand is a mandatory field")
        data = Model.parser.parse_args()

        model = ModelModel(name, data['id_brand'])
        if ModelModel.find_by_name(name.lower()):
            return {"message": "Model with name '{}' "
                               "already exists in the database."
                               .format(name)}, 401
        model.save_to_db()
        return ModelModel.json(ModelModel.find_by_name(name.lower()))
        # a tuple is passed to the json method
        # (object of class model, brand name)

    def delete(self):
        data = Model.parser.parse_args()
        model = ModelModel.find_by_name(data['name'].lower())
        if model:
            model.delete_from_db()
            return {"message": "Model with name '{}' "
                               "has been deleted."
                               .format(data['name'])}, 200
        return {"message": "Model with name '{}' "
                           "does not exist in the database"
                           .format(data['name'])}, 401

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
                [ModelModel.json(model) for model in ModelModel.find_all()]}
