#!/usr/bin/python3
"""
    API states view
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods = ['GET'])
def show_states():
    """Returns json with all states"""
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', strict_slashes=False, methods = ['GET'])
def show_state(state_id):
    """Returns single state from given id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states', strict_slashes=False, methods = ['POST'])
def create_state():
    """Creates new state"""
    state_dict = request.get_json()
    if type(state_dict) is not dict:
        abort(400, 'Not a JSON')
    if 'name' in state_dict:
        state = State(**state_dict)
        state.save()
        return jsonify(state.to_dict()), 201
    abort(400, 'Missing name')


@app_views.route('/states/<state_id>', strict_slashes=False, methods = ['PUT'])
def update_state(state_id):
    """Updates a state from given id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_dict = request.get_json()
    if type(state_dict) is not dict:
        abort(400, 'Not a JSON')
    for k, v in state_dict.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods = ['DELETE'])
def delete_state(state_id):
    """Deletes single state from given id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)

