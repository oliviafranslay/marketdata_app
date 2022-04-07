from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
from models import *
from resources.user import user_bp
from resources.underlying import underlying
from resources.marketdata import marketdata
from security import security
from exception import exception

db.create_all()

# Blueprint
app.register_blueprint(user_bp)
app.register_blueprint(underlying)
app.register_blueprint(security)
app.register_blueprint(marketdata)
app.register_blueprint(exception)

# Run Server
if __name__ == '__main__':
    app.run(port=4000, debug=True)
