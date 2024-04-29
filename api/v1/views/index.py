#!/usr/bin/python3
"""index file where routes to my api are defined"""

from . import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class_objects = {
            "Amenity": Amenity,
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State,
            "User": User
        }


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """returns the status of the api"""
    return jsonify({'status': 'ok'})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """method that returns the number of each objects by type"""
    result = {}
    for key in class_objects:
        result[key] = storage.count(class_objects[key])
    return jsonify(result)
