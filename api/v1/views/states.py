#!/usr/bin/python3
""" AirBnB states Index page """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/', methods=['GET', 'POST'])
@app_views.route('states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_states_routes(state_id=None):
    """ Handle state RESTFul API actions """
    if request.method == 'GET':
        return get_states(state_id)
    elif request.method == 'POST':
        return create_state()
    elif request.method == 'PUT':
        return update_state(state_id)
    elif request.method == 'DELETE':
        return delete_state(state_id)
    else:
        abort(405)


def get_states(state_id):
    """ handle GET request """
    if state_id is None:
        states = [state.to_dict() for state in storage.all("State").values()]
        return jsonify(states)
    else:
        state = storage.get(State, state_id)

        if state is None:
            abort(404)

    return jsonify(state.to_dict())


def create_state():
    """ handle POST request"""
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, 'Missing name')

    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


def update_state(state_id):
    """ handle UPDATE request"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        invalid_keys = ["id", "created_at", "updated_at"]

        if key not in invalid_keys:
            setattr(state, key, value)

    state.save()

    return jsonify(state.to_dict()), 200


def delete_state(state_id):
    """ handle DELETE request"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200
