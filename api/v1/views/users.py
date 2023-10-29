#!/usr/bin/python3
""" AirBnB users Index page """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid


@app_views.route('/users/', methods=['GET', 'POST'])
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_users_routes(user_id=None):
    """ Handle user RESTFul API actions """
    if request.method == 'GET':
        return get_users(user_id)
    elif request.method == 'POST':
        return create_user()
    elif request.method == 'PUT':
        return update_user(user_id)
    elif request.method == 'DELETE':
        return delete_user(user_id)
    else:
        abort(405)


def get_users(user_id):
    """ handle GET request """
    if user_id is None:
        users = [user.to_dict() for user in storage.all("User").values()]
        return jsonify(users)
    else:
        user = storage.get(User, user_id)

        if user is None:
            abort(404)

    return jsonify(user.to_dict())


def create_user():
    """ handle POST request"""
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


def update_user(user_id):
    """ handle UPDATE request"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        invalid_keys = ["id", "email", "created_at", "updated_at"]

        if key not in invalid_keys:
            setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict()), 200


def delete_user(user_id):
    """ handle DELETE request"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200
