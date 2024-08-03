#!/usr/bin/python3
""" view for the link between Place objects and Amenity
objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage, storage_t


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def amenity_by_place_id(place_id):
    """ return the amenities by given place id """
    place = storage.get("Place", place_id)
    amenities = []
    if (place):
        if storage_t == 'db':
            for amenity in place.amenities:
                amenities.append(amenity.to_dict())
        else:
            for amenity in place.amenity_ids:
                amenities.append(amenity.to_dict())
        return jsonify(amenities)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity_linked_by_place(place_id, amenity_id):
    """ delete the amenity by given id """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if (not place or not amenity):
        abort(404)
    if storage_t == 'db' and amenity in place.amenities:
        (place.amenities).remove(amenity)
        storage.save()
        return (jsonify({}), 201)
    if storage_t != 'db' and amenity in place.amenity_ids:
        (place.amenity_ids).remove(amenity.id)
        storage.save()
        return (jsonify({}), 201)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_amenity(place_id, amenity_id):
    """ link amenity to place """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if (not place or not amenity):
        abort(404)
    if storage_t == 'db' and amenity not in place.amenities:
        (place.amenities).append(amenity)
        storage.save()
        return (jsonify(amenity.to_dict()), 201)
    if storage_t != 'db' and amenity not in place.amenity_ids:
        (place.amenity_ids).append(amenity_id)
        storage.save()
        return (jsonify(amenity.to_dict()), 201)
    return (jsonify(amenity.to_dict()), 200)
