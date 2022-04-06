from functools import wraps
from flask import request, jsonify, make_response, Blueprint, Flask
import datetime
import jwt
from models.user import User
from werkzeug.security import check_password_hash
from decouple import config

app = Flask(__name__)
security = Blueprint('security', __name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated_function

# Login
@security.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    person = User.query.filter_by(username=auth.username).first()

    if not person:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    if check_password_hash(person.password, auth.password):
        token = jwt.encode(
            {'public_id': person.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
