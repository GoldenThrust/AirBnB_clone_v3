#!/usr/bin/python3
""" AirBnB places Index page """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from datetime import datetime
import uuid


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_places_in_city_routes(city_id):
    """ Handle places in city routes """
    if request.method == 'GET':
        return get_places_in_city(city_id)
    elif request.method == 'POST':
        return create_place(city_id)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_places_routes(place_id=None):
    """ Handle place RESTFul API actions """
    if request.method == 'GET':
        return get_place(place_id)
    if request.method == 'PUT':
        return update_place(place_id)
    elif request.method == 'DELETE':
        return delete_place(place_id)
    else:
        abort(405)


def get_places_in_city(city_id):
    """ handle GET request """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in
              storage.all("Place").values()
              if city_id == place.city_id]

    return jsonify(places)


def get_place(place_id):
    """ handle GET request """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


def create_place(city_id):
    """ handle POST request"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    if 'name' not in data:
        abort(400, "Missing name")

    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


def update_place(place_id):
    """ handle UPDATE request"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        invalid_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]

        if key not in invalid_keys:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict()), 200


def delete_place(place_id):
    """ handle DELETE request"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200
