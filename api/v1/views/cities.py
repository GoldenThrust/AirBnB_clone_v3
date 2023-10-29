#!/usr/bin/python3
""" AirBnB cities Index page """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'])
def handle_cities_in_city_routes(state_id):
    if request.method == 'GET':
        return get_cities_in_state(state_id)
    elif request.method == 'POST':
        return create_city(state_id)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_cities_routes(city_id=None):
    """ Handle city RESTFul API actions """
    if request.method == 'GET':
        return get_city(city_id)
    if request.method == 'PUT':
        return update_city(city_id)
    elif request.method == 'DELETE':
        return delete_city(city_id)
    else:
        abort(405)


def get_cities_in_state(state_id):
    """ handle GET request """
    city = storage.get(State, state_id)
    if city is None:
        abort(404)

    cities = [city.to_dict() for city in
              storage.all("City").values()
              if state_id == city.state_id]

    return jsonify(cities)


def get_city(city_id):
    """ handle GET request """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


def create_city(state_id):
    """ handle POST request"""
    city = storage.get(City, state_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    if 'name' not in data:
        abort(400, "Missing name")

    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


def update_city(city_id):
    """ handle UPDATE request"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        invalid_keys = ["id", "user_id",
                        "state_id", "created_at", "updated_at"]

        if key not in invalid_keys:
            setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict()), 200


def delete_city(city_id):
    """ handle DELETE request"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200
