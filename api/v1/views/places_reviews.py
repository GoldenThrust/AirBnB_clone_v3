#!/usr/bin/python3
""" AirBnB reviews Index page """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_reviews_in_places_routes(place_id):
    """ Handle reviews in place routes """
    if request.method == 'GET':
        return get_reviews_in_place(place_id)
    elif request.method == 'POST':
        return create_review(place_id)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_reviews_routes(review_id=None):
    """ Handle review RESTFul API actions """
    if request.method == 'GET':
        return get_review(review_id)
    if request.method == 'PUT':
        return update_review(review_id)
    elif request.method == 'DELETE':
        return delete_review(review_id)
    else:
        abort(405)


def get_reviews_in_place(place_id):
    """ handle GET request """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in
               storage.all("Review").values()
               if place_id == review.place_id]

    return jsonify(reviews)


def get_review(review_id):
    """ handle GET request """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


def create_review(place_id):
    """ handle POST request"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if 'text' not in data:
        abort(400, "Missing text")

    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


def update_review(review_id):
    """ handle UPDATE request"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        invalid_keys = ["id", "user_id",
                        "place_id", "created_at", "updated_at"]

        if key not in invalid_keys:
            setattr(review, key, value)

    review.save()

    return jsonify(review.to_dict()), 200


def delete_review(review_id):
    """ handle DELETE request"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200
