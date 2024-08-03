#!/usr/bin/python3
""" view for Review objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def reviews_by_place_id(place_id):
    """ return the reviews by given place id """
    place = storage.get("Place", place_id)
    reviews = []
    if (place):
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)
    abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def review_id(review_id):
    """ return the review by given id """
    review = storage.get("Review", review_id)
    if (review):
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """ delete the review by given id """
    review = storage.get("Review", review_id)
    if (review):
        storage.delete(review)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """ create a new review"""
    place = storage.get("Place", place_id)
    if (place is None):
        abort(404)
    if (not request.is_json):
        abort(400, 'Not a JSON')
    if ('user_id' not in request.get_json()):
        abort(400, 'Missing user_id')
    user = storage.get("User", request.get_json()['user_id'])
    if (user is None):
        abort(404)
    if ('text' not in request.get_json()):
        abort(400, 'Missing text')
    obj = Review(**request.get_json())
    setattr(obj, "place_id", place_id)
    storage.new(obj)
    storage.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """ upade the review by given id """
    ignore_keys = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
    review = storage.get("Review", review_id)

    if (review):
        if (not request.is_json):
            abort(400, 'Not a JSON')
        for key, value in request.get_json().items():
            if (key in ignore_keys):
                continue
            setattr(review, key, value)
        storage.save()
        return (jsonify(review.to_dict()), 200)
    abort(404)
