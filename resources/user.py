from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from datetime import datetime
from sqlalchemy import exc

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
        try:        
           user = UserModel(
                         name,
                         data['email'],
                         UserModel.hash_password(data['password']),
                         datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                         )
           user.save_to_db()
        except exc.IntegrityError as e: # integrity errors from mysql
            return {"message": "{}".format(e.orig.args[1])}, 401
        
        return {"message": "user created successfully"}, 201


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json(), 201
        return {"message": "user not found in the database"}, 404

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db(), 200
            return {
                    "message": "user succesfully deleted from the database"
                   }, 200
        return {"message": "user not found in the database"}, 404


class UserList(Resource):

    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}


class UserLogin(Resource):

    parser = reqparse.RequestParser()

    def post(self, name):
        UserLogin.parser.add_argument("password",
                                       type=str,
                                       required=True,
                                       help="password is a mandatory field")
        data = UserLogin.parser.parse_args()  
        
        user = UserModel.find_by_username(name)

        return UserModel.verify_password(user.password, data["password"])

        if user and safe_str_cmp(user.password, data["password"]):
             access_token = create_access_token(identity=user.id, fresh=True)
             refresh_token = create_refresh_token(user.id)
             return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                 }, 200
        return {"Message": "Invalid credentials"}, 401

