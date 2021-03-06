from db import db
from ma import ma

# Product/Class Model
class Underlying(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True)
    fullname = db.Column(db.String(100), unique=True)
    exchange = db.Column(db.String(50))

    def __init__(self, ticker, fullname, exchange):
        self.ticker = ticker
        self.fullname = fullname
        self.exchange = exchange

    def __repr__(self):
        return '<id {}>'.format(self.id)

# Underlying Schema
class UnderlyingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ticker', 'fullname', 'exchange',)

underlying_schema = UnderlyingSchema()
underlyings_schema = UnderlyingSchema(many=True)

