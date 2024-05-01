#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""

import json
from . import app_views
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET', 'POST'])
def cities(state_id):
    """
    retrieves the list of all City objects of a State using GET method
    and uses POST method to create a city
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')

        if 'name' not in json_data:
            abort(400, 'Missing name')

        new_city = City(**json_data)
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()

        return jsonify(new_city.to_dict()), 201

    city_list = [city.to_dict() for city in state.cities]

    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def cities_by_id(city_id):
    """retrieves a city by its id using GET method
    deletes a city by id using DELETE method
    updates a city data by id using PUT
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()

        return jsonify({}), 200
    elif request.method == 'PUT':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')

        for key, value in json_data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                if hasattr(city, key):
                    setattr(city, key, value)
        storage.save()

        return jsonify(city.to_dict()), 200

    return jsonify(city.to_dict()), 200
