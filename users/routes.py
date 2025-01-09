from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from .models import User
from extensions import db, f
from utils.validator import check_required_fields
users = Blueprint('users', __name__)


@users.errorhandler(404)
def not_exist(err):
    return jsonify({
        'error': 'page does not exist'
    }), 404

@users.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    res = [user.to_json() for user in users]
    return jsonify({
        'success': 'true',
        'datas': res
    })
    
@users.route('/register', methods=['post'])
def register():
    data = request.form
    required_fields = ['username', 'email', 'password', 'alamat']
    empty_fields = check_required_fields(required_fields, data)
    if empty_fields:
        return jsonify({
            'error' : empty_fields
        }), 400
        

    user_exist = User.query.filter_by(email = data.get('email')).first()
    if user_exist:
        return jsonify({
            'error' : 'user already exist'
        }), 400
        
    encrypted_password = f.encrypt(data.get('password').encode()).decode()

    new_user = User(
        username=data.get('username'),
        email=data.get('email'),
        alamat=data.get('alamat'),
        password = encrypted_password
    )
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=data.get('email'))

    return jsonify({
        'success': 'true',
        'token': access_token,
        'data': new_user.to_json()
    }) , 201
    
@users.route('/login', methods=['POST'])
def login():
    data = request.form

    required_fields = ['email', 'password']
    empty_fields = check_required_fields(required_fields, data)
    if empty_fields:
        return jsonify({
            'error' : empty_fields
        }), 400
        

    user_exist = User.query.filter_by(email=data.get('email')).first()
    if not user_exist:
        return jsonify({
            'error': "user doesn't exist"
        }), 404

    decrypted_password = f.decrypt((user_exist.password).encode()).decode()

    if decrypted_password == data.get('password'):
        access_token = create_access_token(data.get('email'))
        return jsonify({
            'success': 'true',
            'message': 'Login successful',
            'password': decrypted_password,
            'access_token': access_token
        })
    else:
        return jsonify({
            'error': 'Invalid password'
        }), 401

@users.route('/delete-account/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_account(id):
    user = User.query.get(id)
    if not user:
        return jsonify({
            'error': "user doesn't exist"
        }), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        'success': 'true',
        'data':user.to_json()
    })

@users.route('/user', methods=['GET', 'PUT'])
@jwt_required()
def single_user():
    method = request.method
    if method == 'GET':
        jwt_identity = get_jwt_identity()
        user = User.query.filter_by(email=jwt_identity).first()

        if not user:
            return jsonify({
                'error': "user doesn't exist"
            }), 404
        
        return jsonify({
            'success': 'true',
            'data': user.to_json()
        })

    if method == 'PUT':
        jwt_identity = get_jwt_identity()
        user = User.query.filter_by(email=jwt_identity).first()

        if not user:
            return jsonify({
                'error': "user doesn't exist"
            }), 404
        
        data = request.form
        user.username = data.get('username')
        user.email = data.get('email')
        
        db.session.commit()

        return jsonify({
            'success': 'true',
            'data':user.to_json()
        })

