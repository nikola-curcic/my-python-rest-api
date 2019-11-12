import os

def add_configs(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://nikola:kovin333@localhost/my_python_rest"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXEPTIONS"] = True
    app.config["APP_ADMIN"] = os.environ.get("APP_ADMIN")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")  
    