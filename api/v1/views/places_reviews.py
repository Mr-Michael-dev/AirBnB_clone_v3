#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Flask route for managing reviews associated with places"""
from flask import jsonify, request, abort
from . import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<string:place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_reviews(place_id):
    """
    Create a new view for handling default RESTful API actions
    related to reviews within a place.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([value.to_dict() for value in place.reviews])
    elif request.method == 'POST':
        request_json = request.get_json()
        if request_json is None or type(request_json) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif request_json.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 400
        elif request_json.get('text') is None:
            return jsonify({'error': 'Missing text'}), 400
        elif storage.get(User, request_json.get('user_id')) is None:
            abort(404)
        new_object = Review(place_id=place_id, **request_json)
        storage.new(new_object)
        storage.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_place_review_id(review_id):
    """Retrieves a review object with a specific ID"""
    review_object = storage.get('Review', review_id)
    if review_object is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(review_object.to_dict())
    elif request.method == 'DELETE':
        review_object = storage.get('Review', review_id)
        storage.delete(review_object)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        insert = request.get_json()
        if insert is None or type(insert) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in insert.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'place_id', 'user_id']:
                if hasattr(review_object, key):
                    setattr(review_object, key, value)
        storage.save()
        return jsonify(review_object.to_dict()), 200
