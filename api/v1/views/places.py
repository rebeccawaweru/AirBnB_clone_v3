#!/usr/bin/python3
"""
updating the place objects that handles all default API actions
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route(
        "/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieve the list of all Place objects of a City:"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrieve a specific place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        "/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """delete a place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route(
        "/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """create a new place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    place = Place(**data)
    place.city_id = city.id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
