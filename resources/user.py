from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from datetime import datetime
from sqlalchemy import exc
from flask_jwt_extended import create_access_token, create_refresh_token
from customdecorators import admin_required

class UserRegister(Resource):

    parser = reqparse.RequestParser()

    def post(self, name):
        UserRegister.parser.add_argument("email",
                                          type=str,
                                          required=True,
                                          help="email is a mandatory field")
        UserRegister.parser.add_argument("password",
                                          type=str,
                                          required=True,
                                          help="password is a mandatory field")
        data = UserRegister.parser.parse_args()  
        # checking if user is admin in UserModel Constructor
        try:        
           user = UserModel(
                         name,
                         data['email'],
                         UserModel.hash_password(data['password']),
                         datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                         )
           user.save_to_db()
        except exc.IntegrityError as e: # integrity errors from mysql
            return {"message": "user with these credentials already registered"}, 401
        
        return {"message": "user created successfully"}, 201


class User(Resource):

    @admin_required
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json(), 201
        return {"message": "user not found in the database"}, 404

    @admin_required
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db(), 200
            return {
                    "message": "user succesfully deleted from the database"
                   }, 200
        return {"message": "user not found in the database"}, 404


class UserList(Resource):

    @admin_required # custom decorator created in file customdecorators
    def get(self):
        return {"users": [user.json() for user in UserModel.find_all()]}


class UserLogin(Resource):

    parser = reqparse.RequestParser()

    def post(self):
        UserLogin.parser.add_argument("username", 
                                       type=str, 
                                       required=True,
                                       help="username is a mandatory field")
        UserLogin.parser.add_argument("password",
                                       type=str,
                                       required=True,
                                       help="password is a mandatory field")
        data = UserLogin.parser.parse_args()     
        user = UserModel.find_by_username(data["username"])  
        if user and UserModel.verify_password(user.password, data["password"]):
            access_token = create_access_token(identity=user.json(), fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                   "access_token": access_token,
                   "refresh_token": refresh_token
                  }, 200
        return {"Message": "Invalid credentials"}, 401

