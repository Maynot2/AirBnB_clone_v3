#!/usr/bin/python3
"""
    API places view
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from os import getenv


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def show_places_per_city(city_id):
    """Returns json with all places for a given city"""
    city = storage.get(City, city_id)
    if city:
        places = city.places
        return jsonify([place.to_dict() for place in places])
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def show_place(place_id):
    """Returns single place from given id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_dict = request.get_json()
    if type(place_dict) is not dict:
        abort(400, 'Not a JSON')
    if 'user_id' not in place_dict:
        abort(400, 'Missing user_id')
    user_id = place_dict['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' in place_dict:
        place = Place(city_id=city_id, **place_dict)
        place.save()
        return jsonify(place.to_dict()), 201
    abort(400, 'Missing name')


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a place from given id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_dict = request.get_json()
    if type(place_dict) is not dict:
        abort(400, 'Not a JSON')
    for k, v in place_dict.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes single place from given id"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)

'''
@app_views.route('/places_search', methods=['POST'])
def place_search():
    """Search places with filters on states/cities and amenities"""
    filters = request.get_json()
    if type(filters) is not dict:
        abort(400, 'Not a JSON')
    list1 = []
    if "states" in filters.keys() and len(filters['states']) != 0:
        filterStates = filters["states"]
        allStates = storage.all(State).values()
        for state in allStates:
            if state.id in filterStates:
                for city in state.cities:
                    for place in city.places:
                        if place not in list1:
                            list1.append(place)
    if "cities" in filters.keys() and len(filters['cities']) != 0:
        filterCities = filters["cities"]
        allCities = storage.all(City).values()
        for city in allCities:
            if city.id in filterCities:
                for place in city.places:
                    if place not in list1:
                        list1.append(place)

    if "states" not in filters.keys() or len(filters['states']) == 0:
        if "cities" not in filters.keys() or len(filters['cities']) == 0:
            list1 = [place for place in storage.all(Place).values()]

    list2 = []

    if "amenities" in filters.keys() and len(filters['amenities']) != 0:
        filterAmenities = filters['amenities']
        setFilt = set(filterAmenities)
        for place in list1:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                placeAmenities = [amenity.id for amenity in place.amenities]
            else:
                placeAmenities = [amen_id for amen_id in place.amenity_ids]
            setAmen = set(placeAmenities)
            if setFilt.issubset(setAmen):
                delattr(place, 'amenities')
                list2.append(place)
    else:
        list2 = list1

    return jsonify([place.to_dict() for place in list2])
'''

@app_views.route('places_search', methods=['POST'])
def retrieve_place_json():
    """Endpoint that retrieves all Place objects
    depending of the JSON in the body of the reques"""
    data = request.get_json(silent=True)
    places = storage.all(Place)
    response = []
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if data != {} and ('states' in data or 'cities' in data):
        if 'state' in data and data['states'] == []:
            if 'cities' in data and data['cities'] == []:
                response = [place for place in places.values()]
        if 'states' in data:
            for state_id in data['states']:
                state = storage.get(State, state_id)
                for city in state.cities:
                    if 'cities' in data and city.id in data['cities']:
                        data['cities'].remove(city.id)
                    for place in city.places:
                        response.append(place)
        if 'cities' in data:
            for city_id in data['cities']:
                city = storage.get(City, city_id)
                for place in city.places:
                    response.append(place)
    else:
        response = [place for place in places.values()]
    if 'amenities' in data:
        response_copy = response.copy()
        for place in response_copy:
            for amenity_id in data['amenities']:
                amenity = storage.get(Amenity, amenity_id)
                if getenv("HBNB_TYPE_STORAGE") == "db":
                    if amenity not in place.amenities:
                        response.remove(place)
                        break
                else:
                    if amenity.id not in place.amenity_ids:
                        response.remove(place)
                        break
    return jsonify([place.to_dict() for place in response])
