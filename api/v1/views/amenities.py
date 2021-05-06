#!/usr/bin/python3
"""
    API amenities view
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def show_amenities():
    """Returns json with all amenities"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def show_amenity(amenity_id):
    """Returns single amenity from given id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates new amenity"""
    amenity_dict = request.get_json()
    if type(amenity_dict) is not dict:
        abort(400, 'Not a JSON')
    if 'name' in amenity_dict:
        amenity = Amenity(**amenity_dict)
        amenity.save()
        return jsonify(amenity.to_dict()), 201
    abort(400, 'Missing name')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a amenity from given id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_dict = request.get_json()
    if type(amenity_dict) is not dict:
        abort(400, 'Not a JSON')
    for k, v in amenity_dict.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes single amenity from given id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)
