#!/usr/bin/python3
"""
    API reviews view
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def show_reviews_per_place(place_id):
    """Returns json with all reviews for a given place"""
    place = storage.get(Place, place_id)
    if place:
        reviews = place.reviews
        return jsonify([review.to_dict() for review in reviews])
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def show_review(review_id):
    """Returns single review from given id"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_dict = request.get_json()
    if type(review_dict) is not dict:
        abort(400, 'Not a JSON')
    if 'user_id' not in review_dict:
        abort(400, 'Missing user_id')
    user_id = review_dict['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' in review_dict:
        review = Review(place_id=place_id, **review_dict)
        review.save()
        return jsonify(review.to_dict()), 201
    abort(400, 'Missing text')


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a review from given id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_dict = request.get_json()
    if type(review_dict) is not dict:
        abort(400, 'Not a JSON')
    for k, v in review_dict.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes single review from given id"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)
