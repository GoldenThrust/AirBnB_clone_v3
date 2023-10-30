#!/usr/bin/python3
""" AirBnB clone Index page """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status')
@app_views.route('/status/')
def status():
    """ returns status """
    status = {
        "status": "OK"
        }

    return jsonify(status)


@app_views.route('/stats')
@app_views.route('/stats/')
def stats():
    """ return stat """
    stats = {}

    for val in classes:
        stats[val] = storage.count(val)

    return jsonify(stats)
