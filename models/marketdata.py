from ma import ma
from db import db


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
    underlying_id = db.Column(db.String(50))

    def __init__(self, date, open, high, low, close, adj_close, volume, underlying_id):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.adj_close = adj_close
        self.volume = volume
        self.underlying_id = underlying_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

# MarketData Schema
class MarketDataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'underlying_id')

marketdata_schema = MarketDataSchema()
marketdatas_schema = MarketDataSchema(many=True)



