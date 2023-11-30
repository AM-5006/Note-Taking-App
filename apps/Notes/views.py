from flask import Flask, request, jsonify, Blueprint, current_app
import jwt
import datetime
from functools import wraps
import bcrypt
from bson import ObjectId, json_util
import json

from database.database import mongo
from .models import Note

notes_routes = Blueprint('Notes', __name__)

def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return func(data['username'], *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401

        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
    return wrapper


@notes_routes.route('/notes', methods=['POST'])
@jwt_required
def create_note(username):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    date_created = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    date_modified = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    note = Note(title=title, content=content, user_id=username, date_created=date_created, date_modified=date_modified)
    mongo.db.Notes.insert_one(note.__dict__)

    return jsonify({'message': 'Note created successfully'}), 201


@notes_routes.route('/notes', methods=['GET'])
@jwt_required
def get_notes(username):
    user_notes = list(mongo.db.Notes.find({'user_id': username}))

    if len(user_notes) == 0:
        return jsonify({'message': 'No notes found'})

    user_notes = json.loads(json_util.dumps(user_notes))
    return jsonify({'notes': user_notes}), 200


@notes_routes.route('/notes/<string:note_id>', methods=['DELETE'])
@jwt_required
def delete_note(username, note_id):
    note = mongo.db.Notes.find_one({'_id': ObjectId(note_id), 'user_id': username})
    if note is None:
        return jsonify({'message': 'Note not found'}), 404

    mongo.db.Notes.delete_one({'_id': ObjectId(note_id)})
    return jsonify({'message': 'Note deleted successfully'})

@notes_routes.route('/notes/<string:note_id>', methods=['PATCH'])
@jwt_required
def update_note(username, note_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    
    note = mongo.db.Notes.find_one({'_id': ObjectId(note_id), 'user_id': username})
    if note is None:
        return jsonify({'message': 'Note not found'}), 404

    update_data = {}
    if title is not None:
        update_data['title'] = title
    if content is not None:
        update_data['content'] = content
    
    update_data['date_modified'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    if update_data:
        mongo.db.Notes.update_one({'_id': ObjectId(note_id)}, {'$set': update_data})
        return jsonify({'message': 'Note updated successfully'}), 200
    else:
        return jsonify({'message': 'No fields to update'}), 400
