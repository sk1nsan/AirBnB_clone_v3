#!/usr/bin/python3
""" index file"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
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
    found = None
    for state in storage.all("State").values():
        if (state.id == state_id):
            found = state
    if (found):
        return jsonify(found.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """ delete the state by given id """
    found = None
    for state in storage.all("State").values():
        if (state.id == state_id):
            found = state
    if (found):
        storage.delete(found)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/states',
                 strict_slashes=False, methods=['POST'])
def create_state():
    """ create a new state"""
    if (not request.get_json()):
        make_response('Not a JSON', 400)
    if ('name' not in request.get_json()):
        make_response('Missing name', 400)
    obj = State(name=request.get_json()['name'])
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """ delete the state by given id """
    found = None
    ignore_keys = ['id', 'created_at', 'updated_at']

    if (not request.get_json()):
        make_response('Not a JSON', 400)
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
