from flask import request, jsonify, Blueprint, Flask
from db import db
from models.user import User, user_schema, users_schema
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
import uuid
from security import token_required

app = Flask(__name__)
user_bp = Blueprint('user_bp', __name__)


# All user information
@user_bp.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = users_schema.dump(users)
    return jsonify({'Users': output})


@user_bp.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})
    return user_schema.jsonify(user)


@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    try:
        new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, admin=True)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "This User already exist in database!"
    return jsonify({'message': 'New user created!'})


@user_bp.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


@user_bp.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User has been deleted'})


