#!/usr/bin/python3
""" AirBnB places Index page """
from models import storage_t
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def handle_amenities_in_places_routes(place_id):
    """ Handle places in city routes """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if storage_t == 'db':
        amenity = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenity)
    else:
        amenity = [amenity.to_dict() for amenity in place.amenity_ids]
        return jsonify(amenity)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'],
                 strict_slashes=False)
def handle_places_amenity_routes(place_id, amenity_id):
    """ Handle place RESTFul API actions """
    if request.method == 'POST':
        return create_place(place_id, amenity_id)
    elif request.method == 'DELETE':
        return delete_place(place_id, amenity_id)
    else:
        abort(405)


def create_place(place_id, amenity_id):
    """ handle POST request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place:
        return jsonify(amenity.to_dict())

    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.append(amenity)
    else:
        if amenity not in place.amenity_ids:
            abort(404)
        place.amenity_ids.append(amenity)

    place.save()
    return jsonify(amenity.to_dict()), 201


def delete_place(place_id, amenity_id):
    """ handle DELETE request"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity)

    storage.save()
    return jsonify({})
