#!/usr/bin/python3
"""
Flask route for managing reviews associated with places
"""
from flask import Blueprint, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<string:place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_reviews_per_place(place_id):
    """Handles requests for reviews associated with a specific place."""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([val.to_dict() for val in place.reviews])
    elif request.method == 'POST':
        post = request.get_json()
        if post is None or type(post) != dict:
            return jsonify({'error': 'Invalid JSON'}), 400
        elif post.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 400
        elif post.get('text') is None:
            return jsonify({'error': 'Missing text'}), 400
        elif storage.get('User', post.get('user_id')) is None:
            abort(404)
        new_review = Review(place_id=place_id, **post)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_place_review_id(review_id):
    """Retrieves a review object with a specific ID"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        review = storage.get('Review', review_id)
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        put = request.get_json()
        if put is None or type(put) != dict:
            return jsonify({'error': 'Invalid JSON'}), 400
        for key, value in put.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'place_id', 'user_id']:
                setattr(review, key, value)
                storage.save()
        return jsonify(review.to_dict()), 200

