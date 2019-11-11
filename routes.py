from flask_restful import Api
from resources.brand import Brand, BrandList
from resources.model import Model, ModelList
from resources.user import User, UserList, UserRegister, UserLogin
from resources.vehicletype import VehicleType, VehicleTypeList


def add_routes(api):
    api.add_resource(Brand, "/brands/<string:name>")
    api.add_resource(BrandList, "/brands")
    api.add_resource(Model, "/models/<string:name>")
    api.add_resource(ModelList, "/models")
    api.add_resource(VehicleType, "/vehicletypes/<string:name>")
    api.add_resource(VehicleTypeList, "/vehicletypes")
    api.add_resource(UserRegister, "/register/<string:name>")
    api.add_resource(User, "/users/<int:user_id>")
    api.add_resource(UserList, "/users")
    api.add_resource(UserLogin, "/login/<string:name>")
    return api
