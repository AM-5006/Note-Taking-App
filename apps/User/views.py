from flask import Flask, request, jsonify, Blueprint, current_app
import bcrypt
from bson import json_util
import json
import jwt
from database.database import mongo
import datetime
from .models import User


user_routes = Blueprint('Users', __name__)

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = mongo.db.User.find_one({'username': username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    username = data['username']
    password = data['password']

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    if mongo.db.User.find_one({'username': username}):
        return jsonify({'message': 'User already exists'}), 400
    user = User(name=name, username=username, password=hashed_password.decode('utf-8'))

    mongo.db.User.insert_one(user.__dict__)
    return jsonify({'message': 'User registered successfully'}), 201

@user_routes.route('/', methods=['GET'])
def get_users():
    all_users = list(mongo.db.User.find({}, {'_id': 0, 'password': 0}))
    if len(all_users) == 0:
        return jsonify({'message': 'No registered users yet'})

    all_users = json.loads(json_util.dumps(all_users))
    return jsonify({'All Users': all_users}), 200
