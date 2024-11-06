from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
     planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

     def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id
             }

class People(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), unique=True, nullable=False)
        favorites = db.relationship("Favorites")

        def serialize(self):
         return {
            "id": self.id,
            "name": self.name
        }

class Planets(db.Model):
        
        id = db.Column(db.Integer, primary_key=True)
        favorites = db.relationship("Favorites")


