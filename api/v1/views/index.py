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


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    """ returns status """
    status = {
        "status": "OK"
        }

    return jsonify(status)


@app_views.route('/stats')
@app_views.route('/stats/')
def stats():
    """ return number of each objects"""
    stats = {}

    for key, val in classes.items():
        stats[key] = storage.count(val)

    return jsonify(stats)
