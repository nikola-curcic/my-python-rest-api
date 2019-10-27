from db import db


class BrandModel(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    models = db.relationship("ModelModel", 
                             lazy="dynamic",    # without dynamic it performs query and returns object
                             backref="parent")  # this way it does not return a result, so all() is necessary
    
    def __init__(self, name):
        self.name = name

    def json(self):
        return {
                'id': self.id,
                'name': self.name,
                'models': [model.json() for model in self.models.all()]
            }

    @classmethod
    def find_by_name(cls, name):
        return db.session.query(cls).filter(cls.name == name).first()

    @classmethod
    def find_by_id(cls, _id):
        return db.session.query(cls).filter(cls.id == _id).first()

    @classmethod
    def find_by_part_of_name(cls, name):
        name = name+"%"
        return db.session.query(cls).filter(cls.name.like(name)).all()

    @classmethod
    def find_all(cls):
        return db.session.query(cls).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def print_models(self):
        print(self.models.all())



