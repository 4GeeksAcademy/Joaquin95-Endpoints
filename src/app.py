"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites,People,Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_hello():
    all_users = User.query.all()
    users = list(map(lambda x: x.serialize(), all_users))
    return jsonify(users), 200

@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_user_fav(id):
    all_favorites = Favorites.query.all(user_id = id)
    fav = list(map(lambda x: x.serialize(), all_favorites))
    return jsonify(fav), 200

@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def post_favorite_people(user_id, people_id):
    favorite = Favorites(user_id = user_id, people_id = people_id, Planet_id = "NULL")
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite), 200

@app.route('/users/<int:user_id>/favorites/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet(user_id, planet_id):
    favorite = Favorites(user_id=user_id, people_id=None, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200


@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    people = Favorites.query.filter_by(user_id = user_id, people_id = people_id).first()
    db.session.delete(people)
    db.session.commit()
    return jsonify("You deleted favorite people")

@app.route('/users/<int:user_id>/favorites/people/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    planet = Favorites.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    db.session.delete(planet)
    db.session.commit()
    return jsonify("You deleted favorite planet")


@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = People.query.all()
    people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(people), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_each_people(people_id):
    people = people.query.filter_by.id(id = people_id).first()
    return jsonify(people)

@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planets.query.all()
    planets = list(map(lambda x: x.serialize(), all_planets))
    return jsonify(planets), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_each_planets(planet_id):
    planet = planet.query.filter_by.id(id = planet_id).first()
    return jsonify(planet)

@app.route('/people', methods=['POST'])
def get_people():
    data = request.get_json()
    people = People(name = data ['name'],)
    db.session.add(people)
    db.session.commit()
    return jsonify(people.serialize()), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
