#!/usr/bin/python3
""" Create route /status """
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ API status """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """retrieves the number of each object by types"""
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(data)
