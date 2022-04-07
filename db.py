from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

# Init db
db = SQLAlchemy(app)
