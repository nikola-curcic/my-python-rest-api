from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from datetime import datetime


_user_parser = reqparse.RequestParser()


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        user = UserModel(
                         data['username'],
                         UserModel.hash_password(data['password']),
                         datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                         )
        user.save_to_db()
        result = UserModel.find_all()
        for row in result:
            print(row.json())
        return {"message": "user created successfully"}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json(), 201
        return {"message": "user not found in the database"}, 401

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db(), 200
            return {
                    "message": "user succesfully deleted from the database"
                   }, 200
        return {"message": "user not found in the database"}, 401


class UserList(Resource):

    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
             access_token = create_access_token(identity=user.id, fresh=True)
             refresh_token = create_refresh_token(user.id)
             return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                 }, 200
        return {"Message": "Invalid credentials"}, 401

