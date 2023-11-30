from flask import Flask, request, jsonify, Blueprint, current_app, session, redirect, url_for
import bcrypt
from bson import json_util
import json
import jwt
from database.database import mongo
import datetime
from .models import User
import hashlib

user_routes = Blueprint('Users', __name__)

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data['identifier']
    password = data['password']

    user = mongo.db.User.find_one({
        '$or': [
            {'email': identifier},
            {'username': identifier}
        ]
    })
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        token = jwt.encode({'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        session['user_logged_in'] = True
        session['user_details'] = {
            'name':user['name'],
            'username':user['username'],
            'email':user['email']
        }
        session['token'] = token
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    if mongo.db.User.find_one({'email': email}):
        return jsonify({'message': 'Email already in use'}), 400

    hash_object = hashlib.md5(email.encode())
    unique_number = int(hash_object.hexdigest(), 16) % 9000 + 1000

    username = f"{name.lower().replace(' ', '_')}_{unique_number}"
    user = User(name=name, email=email, username=username, password=hashed_password.decode('utf-8'))

    mongo.db.User.insert_one(user.__dict__)
    return jsonify({'message': 'User registered successfully'}), 201


@user_routes.route('/admin', methods=['GET'])
def get_users():
    all_users = list(mongo.db.User.find({}, {'_id': 0, 'password': 0}))
    if len(all_users) == 0:
        return jsonify({'message': 'No registered users yet'})

    all_users = json.loads(json_util.dumps(all_users))
    return jsonify({'All Users': all_users}), 200

