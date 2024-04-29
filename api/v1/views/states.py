#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""

import json
from . import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states():
    """
    retrieves the list of all state objects using GET method
    and uses POST method to add a state to the states list
    """
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')

        if 'name' not in json_data:
            abort(400, 'Missing name')

        new_state = State(**json_data)
        storage.new(new_state)
        storage.save()

        return jsonify(new_state.to_dict()), 201

    all_states = storage.all(State)
    state_list = [state.to_dict() for state in all_states.values()]

    return jsonify(state_list), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state_by_id(state_id):
    """
    retrieves a state by its id using GET method
    deletes a state by id using DELETE method
    updates a state data by id using PUT
    """
    if request.method == 'DELETE':
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        storage.delete(state)
        storage.save()

        return jsonify({}), 200
    elif request.method == 'PUT':
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')

        for key, value in json_data.items():
            if key != 'id' or key != 'created_at' or key != 'updated_at':
                if hasattr(state, key):
                    setattr(state, key, value)
        storage.save()

        return jsonify(state.to_dict()), 200

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict()), 200
