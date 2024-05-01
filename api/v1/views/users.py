#!/usr/bin/python3
"""view for User objects that handles all default RESTFul API actions"""

from . import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users():
    """
    retrieves the list of all user objects using GET method
    and uses POST method to add a user to the users list
    """
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')

        if 'name' not in json_data:
            abort(400, 'Missing name')

        new_user = User(**json_data)
        storage.new(new_user)
        storage.save()

        return jsonify(new_user.to_dict()), 201

    all_user = storage.all(User)
    user_list = [user.to_dict() for user in all_user.values()]

    return jsonify(user_list), 200


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_by_id(user_id):
    """
    retrieves a user by its id using GET method
    deletes a user by id using DELETE method
    updates a user data by id using PUT
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()

        return jsonify({}), 200
    elif request.method == 'PUT':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')

        for key, value in json_data.items():
            if key not in ['id', 'email' 'created_at', 'updated_at']:
                if hasattr(user, key):
                    setattr(user, key, value)
        storage.save()

        return jsonify(user.to_dict()), 200

    return jsonify(user.to_dict()), 200
