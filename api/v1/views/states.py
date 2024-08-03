#!/usr/bin/python3
""" index file"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def states():
    """ return list of all State objects """
    all_states = []
    for state in storage.all("State").values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['GET'])
def state_id(state_id):
    """ return the state by given id """
    state = storage.get("State", state_id)
    if (state):
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """ delete the state by given id """
    state = storage.get("State", state_id)
    if (state):
        storage.delete(state)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/states',
                 strict_slashes=False, methods=['POST'])
def create_state():
    """ create a new state"""
    if (not request.is_json):
        abort(400, 'Not a JSON')
    if ('name' not in request.get_json()):
        abort(400, 'Missing name')
    obj = State(**request.get_json())
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """ delete the state by given id """
    found = None
    ignore_keys = ['id', 'created_at', 'updated_at']

    if (not request.is_json):
        abort(400, 'Not a JSON')
    for state in storage.all("State").values():
        if (state.id == state_id):
            found = state
    if (found):
        for key, value in request.get_json().items():
            if (key in ignore_keys):
                continue
            setattr(found, key, value)
        storage.save()
        return (jsonify(found.to_dict()), 200)
    abort(404)
