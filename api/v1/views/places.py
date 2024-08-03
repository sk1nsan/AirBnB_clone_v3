#!/usr/bin/python3
""" view for Place objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def places_by_city_id(city_id):
    """ return the places by given city id """
    city = storage.get("City", city_id)
    places = []
    if (city):
        for place in city.places:
            places.append(place.to_dict())
        return jsonify(places)
    abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET'])
def place_id(place_id):
    """ return the place by given id """
    place = storage.get("Place", place_id)
    if (place):
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """ delete the place by given id """
    place = storage.get("Place", place_id)
    if (place):
        storage.delete(place)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """ create a new place"""
    city = storage.get("City", city_id)
    if (city is None):
        abort(404)
    if (not request.is_json):
        abort(400, 'Not a JSON')
    user = storage.get("User", request.get_json()['user_id'])
    if (user is None):
        abort(400, 'Missing user_id')
    if ('name' not in request.get_json()):
        abort(400, 'Missing name')
    obj = Place(**request.get_json())
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ upade the place by given id """
    ignore_keys = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']

    if (not request.is_json):
        abort(400, 'Not a JSON')
    place = storage.get("Place", place_id)
    if (place):
        for key, value in request.get_json().items():
            if (key in ignore_keys):
                continue
            setattr(place, key, value)
        storage.save()
        return (jsonify(place.to_dict()), 200)
    abort(404)
