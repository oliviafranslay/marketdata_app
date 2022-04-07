from db import db
from ma import ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    admin = db.Column(db.Boolean)


    def __init__(self, public_id, username, password, admin):
        self.public_id = public_id
        self.username = username
        self.password = password
        self.admin = admin

    def __repr__(self):
        return '<id {}>'.format(self.id)

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'username', 'password', 'admin')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
