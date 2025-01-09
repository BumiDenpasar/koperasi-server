from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from .models import Transaction
from users.models import User
from extensions import db, f
from utils.validator import check_required_fields
transactions = Blueprint('transactions', __name__)


@transactions.route('/transactions', methods=['GET'])
@jwt_required()
def get_all_transactions():
    jwt_identity = get_jwt_identity()
    user = User.query.filter_by(email = jwt_identity).first()
    if not user:
        return jsonify({
            'error': "Token not valid"
        }), 404
    
    transactions = Transaction.query.filter_by(user_id = user.id).all()
    res = [transaction.to_json() for transaction in transactions]
    return jsonify({
        'success': 'true',
        'datas': res
    })

@transactions.route('/transactions/<int:id>', methods=['GET', 'DELETE'])
@jwt_required()
def single_transaction(id):
    method = request.method

    jwt_identity = get_jwt_identity()
    user = User.query.filter_by(email = jwt_identity).first()
    if not user:
        return jsonify({
            'error': "Token not valid"
        }), 400
    
    if method == 'GET':
        transaction = Transaction.query.filter_by(id = id, user_id = user.id).first()
        if not transaction:
            return jsonify({
                'error': "Transaction not found"
            }), 400
        return jsonify({
            'success': 'true',
            'datas': transaction.to_json()
        })
    
    if method == 'DELETE':
        transaction = Transaction.query.filter_by(id = id, user_id = user.id).first()
        if not transaction:
            return jsonify({
                "error": "transaction not found"
            }), 400
        db.session.delete(transaction)
        db.session.commit()

        return jsonify({
            'success': 'true',
        }), 200

@transactions.route('/transactions/add', methods=['POST'])
@jwt_required()
def add_transaction():
    data = request.json
    jwt_identity = get_jwt_identity()
    user = User.query.filter_by(email = jwt_identity).first()
    if not user:
        return jsonify({
            'error': "Token not valid"
        }), 400

    print(data)
    required_fields = ['jumlah', 'jenis']
    empty_field = check_required_fields(required_fields, data)
    if empty_field:
        return jsonify({
            'error': empty_field
        }), 400
    
    new_transaction = Transaction(
        user_id = user.id,
        jumlah = data.get('jumlah'),
        jenis = data.get('jenis'),
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({
        'success': 'true',
        'data': new_transaction.to_json()
    }) , 201