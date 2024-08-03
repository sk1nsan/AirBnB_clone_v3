#!/usr/bin/python3
""" view for amenity objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 strict_slashes=False, methods=['GET'])
def amenities():
    """ return all amenities """
    amenities = []
    for amenity in storage.all('Amenity').values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def amenity_id(amenity_id):
    """ return the amenity by given id """
    amenity = storage.get("Amenity", amenity_id)
    if (amenity):
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete the amenity by given id """
    amenity = storage.get("Amenity", amenity_id)
    if (amenity):
        storage.delete(amenity)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/amenities',
                 strict_slashes=False, methods=['POST'])
def create_amenity():
    """ create a new Amenity"""
    if (not request.is_json):
        abort(400, 'Not a JSON')
    if ('name' not in request.get_json()):
        abort(400, 'Missing name')
    obj = Amenity(**request.get_json())
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """ upade the amenity by given id """
    ignore_keys = ['id', 'created_at', 'updated_at']

    if (not request.is_json):
        abort(400, 'Not a JSON')
    amenity = storage.get("Amenity", amenity_id)
    if (amenity):
        for key, value in request.get_json().items():
            if (key in ignore_keys):
                continue
            setattr(amenity, key, value)
        storage.save()
        return (jsonify(amenity.to_dict()), 200)
    abort(404)
