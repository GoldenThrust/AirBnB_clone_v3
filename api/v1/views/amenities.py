#!/usr/bin/python3
""" AirBnB amenitys Index page """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
# from datetime import datetime
# import uuid


@app_views.route('/amenities/', methods=['GET', 'POST'])
@app_views.route('amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_amenitys_routes(amenity_id=None):
    """ Handle amenity RESTFul API actions """
    if request.method == 'GET':
        return get_amenities(amenity_id)
    elif request.method == 'POST':
        return create_amenity()
    elif request.method == 'PUT':
        return update_amenity(amenity_id)
    elif request.method == 'DELETE':
        return delete_amenity(amenity_id)
    else:
        abort(405)


def get_amenities(amenity_id):
    """ handle GET request """
    if amenity_id is None:
        amenities = [amenity.to_dict()
                     for amenity in storage.all("Amenity").values()]
        return jsonify(amenities)
    else:
        amenity = storage.get(Amenity, amenity_id)

        if amenity is None:
            abort(404)

    return jsonify(amenity.to_dict())


def create_amenity():
    """ handle POST request"""
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, 'Missing name')

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


def update_amenity(amenity_id):
    """ handle UPDATE request"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        invalid_keys = ["id", "created_at", "updated_at"]

        if key not in invalid_keys:
            setattr(amenity, key, value)

    amenity.save()

    return jsonify(amenity.to_dict()), 200


def delete_amenity(amenity_id):
    """ handle DELETE request"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
