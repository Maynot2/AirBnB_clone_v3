#!/usr/bin/python3
"""
    API cities view
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def show_cities_per_state(state_id):
    """Returns json with all cities for a given state"""
    state = storage.get(State, state_id)
    if state:
        cities = state.cities
        return jsonify([city.to_dict() for city in cities])
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def show_city(city_id):
    """Returns single city from given id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_dict = request.get_json()
    if type(city_dict) is not dict:
        abort(400, 'Not a JSON')
    if 'name' in city_dict:
        city = City(state_id=state_id, **city_dict)
        city.save()
        return jsonify(city.to_dict()), 201
    abort(400, 'Missing name')


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city from given id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city_dict = request.get_json()
    if type(city_dict) is not dict:
        abort(400, 'Not a JSON')
    for k, v in city_dict.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes single city from given id"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)
