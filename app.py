from flask import Flask
from flask_restful import Api
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from resources.brand import Brand, BrandList
from resources.model import Model, ModelList
from resources.user import User, UserList
from resources.vehicletype import VehicleType, VehicleTypeList
import pymysql

    
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://nikola:kovin333@localhost/my_python_rest"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)
manager = Manager(app)


api.add_resource(Brand, "/brands/<string:name>")
api.add_resource(BrandList, "/brands")
api.add_resource(Model, "/models/<string:name>")
api.add_resource(ModelList, "/models")
api.add_resource(VehicleType, "/vehicletypes/<string:name>")
api.add_resource(VehicleTypeList, "/vehicletypes")



if __name__ == "__main__":
    from db import db
    db.init_app(app)
    migrate = Migrate(app, db)
    manager.add_command('db',MigrateCommand)
    manager.run()

