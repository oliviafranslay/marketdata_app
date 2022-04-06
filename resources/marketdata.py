from models.marketdata import MarketData, marketdata_schema, marketdatas_schema
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError
from db import db
from security import token_required

marketdata = Blueprint('marketdata', __name__)

# Create an MarketData
@marketdata.route('/marketdata/<underlying_id>', methods=['GET'])
def get_all_marketdata(underlying_id):
    stocks = MarketData.query.filter_by(underlying_id=underlying_id).all()
    output = marketdatas_schema.dump(stocks)
    return jsonify({'Market Data': output})


@marketdata.route('/marketdata/<underlying_id>/<date>', methods=['GET'])
def get_one_marketdata(underlying_id, date):
    stock = MarketData.query.filter_by(underlying_id=underlying_id, date=date).first()

    if not stock:
        return jsonify({'message': 'No stock found!'})
    output = marketdata_schema.dump(stock)
    return jsonify({underlying_id: output})

@marketdata.route('/marketdata/<underlying_ticker>', methods=['POST'])
@token_required
def add_marketdata(current_user, underlying_ticker):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    data = request.get_json()
    new_marketdata = MarketData(date=data['date'], open=data['open'], high=data['high'],
                                low=data['low'], close=data['close'], adj_close=data['adj_close'],
                                volume=data['volume'], underlying_id=underlying_ticker)
    db.session.add(new_marketdata)
    db.session.commit()

    return jsonify({'message': "Market Data created!"})

@marketdata.route('/marketdata/<underlying_id>/<date>', methods=['PUT'])
@token_required
def update_marketdata(current_user, underlying_id, date):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    try:
        stock = MarketData.query.filter_by(underlying_id=underlying_id, date=date).first()

        date = request.json['date']
        open = request.json['open']
        high = request.json['high']
        low = request.json['low']
        close = request.json['close']
        adj_close = request.json['adj_close']
        volume = request.json['volume']

        stock.date = date
        stock.open = open
        stock.high = high
        stock.low = low
        stock.close = close
        stock.adj_close = adj_close
        stock.volume = volume

        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Duplicate input!"
    return marketdata_schema.jsonify(stock)

@marketdata.route('/marketdata/<underlying_id>/<date>', methods=['DELETE'])
@token_required
def remove_marketdata(current_user, underlying_id, date):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'}), 403

    stock = MarketData.query.filter_by(underlying_id=underlying_id, date=date).first()

    if not stock:
        return jsonify({'message': 'No stock found!'})

    db.session.delete(stock)
    db.session.commit()

    return jsonify({'message': 'Stock item deleted!'})