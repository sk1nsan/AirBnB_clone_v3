#!/usr/bin/python3
""" view for user objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users',
                 strict_slashes=False, methods=['GET'])
def users():
    """ return all users """
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)
    abort(404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['GET'])
def user_id(user_id):
    """ return the user by given id """
    user = storage.get("User", user_id)
    if (user):
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """ delete the user by given id """
    user = storage.get("User", user_id)
    if (user):
        storage.delete(user)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/users',
                 strict_slashes=False, methods=['POST'])
def create_user():
    """ create a new User"""
    if (not request.is_json):
        abort(400, 'Not a JSON')
    if ('name' not in request.get_json()):
        abort(400, 'Missing name')
    if ('email' not in request.get_json()):
        abort(400, 'Missing email')
    if ('password' not in request.get_json()):
        abort(400, 'Missing password')
    obj = User(**request.get_json())
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """ upade the user by given id """
    ignore_keys = ['id', 'created_at', 'updated_at']

    if (not request.is_json):
        abort(400, 'Not a JSON')
    user = storage.get("User", user_id)
    if (user):
        for key, value in request.get_json().items():
            if (key in ignore_keys):
                continue
            setattr(user, key, value)
        storage.save()
        return (jsonify(user.to_dict()), 200)
    abort(404)
