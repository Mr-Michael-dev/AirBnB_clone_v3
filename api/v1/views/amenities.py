#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions"""

from . import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenities():
    """
    retrieves the list of all amenity objects using GET method
    and uses POST method to add an amenity to the amenities list
    """
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data or type(json_data) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in json_data:
            return jsonify({'error': 'Missing name'}), 400

        new_amenity = Amenity(**json_data)
        storage.new(new_amenity)
        storage.save()

        return jsonify(new_amenity.to_dict()), 201

    all_amenities = storage.all(Amenity)
    amenity_list = [amenity.to_dict() for amenity in all_amenities.values()]

    return jsonify(amenity_list), 200


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_by_id(amenity_id):
    """
    retrieves an amenity by its id using GET method
    deletes a amenity by id using DELETE method
    updates a amenity data by id using PUT
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()

        return jsonify({}), 200
    elif request.method == 'PUT':
        json_data = request.get_json()
        if not json_data or type(json_data) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400

        for key, value in json_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                if hasattr(amenity, key):
                    setattr(amenity, key, value)
        storage.save()

        return jsonify(amenity.to_dict()), 200

    return jsonify(amenity.to_dict()), 200
