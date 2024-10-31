from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    decode_token,
    jwt_required,
    get_jwt,
    set_access_cookies,
    unset_jwt_cookies
)
from extensions import db, jwt, redis_client
from models import User
from datetime import timedelta, datetime

auth = Blueprint('auth', __name__)

@jwt.token_in_blocklist_loader
def check_if_token_is_valid(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = redis_client.get(jti)
    return token_in_redis is None

def store_token_in_redis(access_token):
    decoded_token = decode_token(access_token)
    jti = decoded_token["jti"]
    exp_timestamp = decoded_token["exp"]
    
    ttl = exp_timestamp - datetime.timestamp(datetime.now())
    redis_client.setex(jti, int(ttl), 'valid')

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already taken'}), 400
        
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        
        access_token = create_access_token(
            identity=new_user.id,
            expires_delta=timedelta(hours=1)
        )

        store_token_in_redis(access_token)
        
        response = jsonify({
            'message': 'User registered successfully',
            'user_id': new_user.id
        })

        set_access_cookies(response, access_token)
        
        return response, 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 400

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=1)
        )

        store_token_in_redis(access_token)
        
        response = jsonify({
            'message': 'Login successful',
            'user_id': user.id
        })

        set_access_cookies(response, access_token)
        
        return response, 200
        
    return jsonify({'message': 'Invalid credentials'}), 401

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]

    redis_client.delete(jti)
    
    response = jsonify({'message': 'Successfully logged out'})
    unset_jwt_cookies(response)
    return response, 200

@auth.cli.command('check-redis')
def check_redis():
    """Check if Redis is connected and working."""
    try:
        redis_client.ping()
        print("Successfully connected to Redis!")
    except Exception as e:
        print(f"Failed to connect to Redis: {str(e)}")