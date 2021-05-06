#!/usr/bin/python3
"""
    API users view
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def show_users():
    """Returns json with all users"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'])
def show_user(user_id):
    """Returns single user from given id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates new user"""
    user_dict = request.get_json()
    if type(user_dict) is not dict:
        abort(400, 'Not a JSON')
    if 'email' not in user_dict:
        abort(400, 'Missing email')
    if 'password' not in user_dict:
        abort(400, 'Missing password')
    user = User(**user_dict)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a user from given id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_dict = request.get_json()
    if type(user_dict) is not dict:
        abort(400, 'Not a JSON')
    for k, v in user_dict.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes single user from given id"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)
