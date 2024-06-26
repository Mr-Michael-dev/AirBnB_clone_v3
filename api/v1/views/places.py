#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from flask import jsonify, request, abort
from . import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_per_city(city_id):
    """Handles requests related to places within a city."""
    city_object = storage.get(City, city_id)
    if not city_object:
        abort(404)
    if request.method == 'GET':
        return jsonify([value.to_dict() for value in city_object.places])
    elif request.method == 'POST':
        request_json = request.get_json()
        if request_json is None or type(request_json) is not dict:
            return jsonify({'error': 'Invalid JSON format'}), 400
        elif request_json.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400
        elif request_json.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'}), 400
        elif storage.get(User, request_json.get('user_id')) is None:
            abort(404)
        new_object = Place(city_id=city_id, **request_json)
        storage.new(new_object)
        storage.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def find_place_id(place_id):
    """Retrieves a place object with a specific id"""
    place_object = storage.get(Place, place_id)
    if not place_object:
        abort(404)
    if request.method == 'GET':
        return jsonify(place_object.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(place_object)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        insert = request.get_json()
        if insert is None or type(insert) is not dict:
            return jsonify({'error': 'Invalid JSON format'}), 400
        for key, value in insert.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'city_id', 'user_id']:
                if hasattr(place_object, key):
                    setattr(place_object, key, value)
        storage.save()
        return jsonify(place_object.to_dict()), 200
