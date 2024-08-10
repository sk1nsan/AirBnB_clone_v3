#!/usr/bin/python3
""" index file"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {"amenities": "Amenity", "cities": "City",
           "places": "Place", "reviews": "Review",
           "states": "State", "users": "User"}


@app_views.route('/status')
def status():
    """ return the status of the api """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ return the "number of each objects by type """
    result = {}
    for key, value in classes.items():
        result[key] = storage.count(value)
    return jsonify(result)
