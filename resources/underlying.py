from models.underlying import underlying_schema, underlyings_schema, Underlying
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError
from db import db
from security import token_required

underlying = Blueprint('underlying', __name__)

# Create an Underlying
@underlying.route('/underlying', methods=['GET'])
def get_all_underlying():
    stocks = Underlying.query.all()
    output = underlyings_schema.dump(stocks)
    return jsonify({'Underlying': output})

@underlying.route('/underlying/<stock_id>', methods=['GET'])
def get_one_stock(stock_id):
    stock = Underlying.query.filter_by(id=stock_id).first()

    if not stock:
        return jsonify({'message': 'No stock found!'})
    return underlying_schema.jsonify(stock)

@underlying.route('/underlying', methods=['POST'])
@token_required
def add_stock(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    data = request.get_json()

    new_stock = Underlying(ticker=data['ticker'], fullname=data['fullname'], exchange=data['exchange'])
    db.session.add(new_stock)
    db.session.commit()

    return jsonify({'message' : "Stock created!"})

@underlying.route('/underlying/<stock_id>', methods=['PUT'])
@token_required
def update_stock(current_user, stock_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    try:
        stock = Underlying.query.filter_by(id=stock_id).first()

        ticker = request.json['ticker']
        fullname = request.json['fullname']
        exchange = request.json['exchange']

        stock.ticker = ticker
        stock.fullname = fullname
        stock.exchange = exchange

        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Duplicate input!"
    return underlying_schema.jsonify(stock)

@underlying.route('/underlying/<stock_id>', methods=['DELETE'])
@token_required
def remove_stock(current_user, stock_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    stock = Underlying.query.filter_by(id=stock_id).first()

    if not stock:
        return jsonify({'message' : 'No stock found!'})

    db.session.delete(stock)
    db.session.commit()

    return jsonify({'message' : 'Stock item deleted!'})