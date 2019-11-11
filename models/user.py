import hashlib
import binascii
import os
from db import db
from flask import current_app

class UserModel(db.Model):
    __tablename__ ='users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(192))
    time_created = db.Column(db.String(25))
    user_level = db.Column(db.String(5))

    def __init__(self, username, email, password, time_created):
        self.username = username
        self.email = email
        self.password = password
        self.time_created = time_created
        if self.email == current_app.config['APP_ADMIN']:
            self.user_level = 'admin'
        else:
            self.user_level = 'user'
            

    def json(self):
        return {
               "id": self.id,
               "name": self.username,
               "time_created": self.time_created,
               "user_level": self.user_level
            }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def hash_password(cls, password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    @classmethod
    def verify_password(cls, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                    provided_password.encode('utf-8'),
                                    salt.encode('ascii'),
                                    100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
   
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()









