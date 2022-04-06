from db import db
from ma import ma

# Market Data Model
class MarketData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer)
    open = db.Column(db.Integer)
    high = db.Column(db.Integer)
    low = db.Column(db.Integer)
    close = db.Column(db.Integer)
    adj_close = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    underlying_id = db.Column(db.Integer, db.ForeignKey('underlying.id'), nullable=False)

# MarketData Schema
class MarketDataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'underlying_id')

marketdata_schema = MarketDataSchema()
marketdatas_schema = MarketDataSchema(many=True)