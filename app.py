from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from resources.user import user
from resources.underlying import underlying
from security import security
from resources.marketdata import marketdata
from exception import exception
from decouple import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')

# Init db
db = SQLAlchemy(app)

# Create table
db.create_all()

# Blueprint
app.register_blueprint(user)
app.register_blueprint(underlying)
app.register_blueprint(security)
app.register_blueprint(marketdata)
app.register_blueprint(exception)

# Run Server
if __name__ == '__main__':
    app.run(port=4000, debug=True)
