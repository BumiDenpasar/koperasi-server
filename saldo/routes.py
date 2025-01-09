from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from .models import Saldo
from users.models import User
from extensions import db, f
from utils.validator import check_required_fields
saldo = Blueprint('saldo', __name__, url_prefix='/saldo')

@saldo.route('/', methods=['GET'])
@jwt_required()
def get_current_saldo():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({
            'error' : 'token is not valid'
        })
    saldo = Saldo.query.filter_by(user_id=user.id).first()
    return jsonify({
        'success': 'true',
        'data': saldo.to_json(),
    })
