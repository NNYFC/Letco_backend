import json
import datetime
import os
from functools import wraps

import bcrypt
import jwt
from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

from src.config.connection_db import DbConnection
from src.model.db_model import Role, User

application = Flask(__name__)
application.config['SECRET'] = 'token secret'

hostname = os.environ.get('db_hostname')
dbname = os.environ.get('db_name')
username = os.environ.get('db_username')
password = os.environ.get('db_password')

engine = DbConnection(hostname, dbname, username, password)
factory = sessionmaker(bind=engine.connect())
session = factory()


# Authentication decorator
def token_required(f, role="GUESS"):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if 'Authorization' in request.headers:
            auth = request.headers['Authorization']
            token = auth.split()
        if not token: # throw error if no token provided
            return jsonify({"message": "A valid token is missing!"}), 401
        try:
            # decode the token to obtain user public_id
            decoded_token = jwt.decode(token, key=application.config['SECRET'], algorithms=['HS256'])
            current_user = session.get(entity=User, ident=decoded_token['unique'])
            if current_user.role != role:
                return jsonify({"message": "Don't have enough permission"}), 401
        except Exception as e:
            return jsonify({"message": "Invalid token! "+f'{e}'}), 401
        # Return the user information attached to the token
        return f(current_user, *args, **kwargs)
    return decorator


@application.route('/', methods=['GET'])
def welcome_endpoint():
    return json.dumps({'message': 'Welcome to LETCO API'})


@application.route('/register', methods=['POST'])
def registration():
    data = json.loads(request.data)
    print(data)
    role = session.get(entity=Role, ident=data['idrole'])
    # Adding the salt to password
    salt = bcrypt.gensalt()
    # Hashing the password
    hashed = bcrypt.hashpw(data['password'], salt)
    user = User(name=data['name'], pseudo=data['pseudo'], email=data['email'],
                password=hashed, bluetooth=data['bluetooth'], idrole=role.id)
    session.add(user)
    session.commit()
    session.flush()
    users = session.query(User).all()
    print(user)
    return application.response_class(response=json.dumps(user, cls=AlchemyEncoder),
                                      status=201, content_type='application/json')


@application.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    print(data)
    user = session.get(entity=User, ident=data['email'])
    pwd_check = bcrypt.checkpw(data['password'], user.password)
    login_repond = []
    status = 403
    if pwd_check:
        token = jwt.encode({'unique': user.email, "exp": datetime.timedelta(hours=24)},
                           key=application.config['SECRET'], algorithm=['HS256'])
        login_repond = {
            'token': token,
            'data': user
        }
        status = 200
        # print(users)
    return application.response_class(response=json.dumps(login_repond, cls=AlchemyEncoder),
                                      status=status, content_type='application/json')


@application.route('/users', methods=['GET'])
@token_required("CLIENT")
def get_all_users():
    users = session.query(User).all()
    print(users)
    print(type(users))
    return application.response_class(response=json.dumps(users, cls=AlchemyEncoder),
                                      status=200, content_type='application/json')


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True, port=8000)
