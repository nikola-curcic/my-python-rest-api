from flask import Flask
from flask_restful import Api
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from routes import add_routes  # routes added in a separate file
from config import add_configs  # configs added in a separate file
from db import db
from flask_jwt_extended import JWTManager


app = Flask(__name__)

add_configs(app)
api = add_routes(Api(app))
manager = Manager(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()

