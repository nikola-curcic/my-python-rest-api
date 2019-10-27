from flask import Flask
from flask_restful import Api
from resources.brand import Brand, BrandList
from resources.model import Model, ModelList


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Brand, "/brands/<string:name>")
api.add_resource(BrandList, "/brands")
api.add_resource(Model, "/models/<string:name>")
api.add_resource(ModelList, "/models")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)