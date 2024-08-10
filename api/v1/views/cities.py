#!/usr/bin/python3
""" view for City objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def cities_by_state_id(state_id):
    """ return the cities by given state id """
    state = storage.get("State", state_id)
    cities = []
    if (state):
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['GET'])
def city_id(city_id):
    """ return the city by given id """
    city = storage.get("City", city_id)
    if (city):
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """ delete the city by given id """
    city = storage.get("City", city_id)
    if (city):
        storage.delete(city)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """ create a new City"""
    state = storage.get("State", state_id)
    if (state is None):
        abort(404)
    if (not request.is_json):
        abort(400, 'Not a JSON')
    if ('name' not in request.get_json()):
        abort(400, 'Missing name')
    obj = City(**request.get_json())
    setattr(obj, "state_id", state_id)
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ upade the city by given id """
    ignore_keys = ['id', 'created_at', 'updated_at', 'state_id']

    if (not request.is_json):
        abort(400, 'Not a JSON')
    city = storage.get("City", city_id)
    if (city):
        for key, value in request.get_json().items():
            if (key in ignore_keys):
                continue
            setattr(city, key, value)
        storage.save()
        return (jsonify(city.to_dict()), 200)
    abort(404)
