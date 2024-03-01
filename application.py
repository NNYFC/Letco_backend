import json
from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

from src.config.connection_db import DbConnection
from src.model.db_model import Role, User

application = Flask(__name__)

hostname = ''
dbname = ''
username = ''
password = ''

engine = DbConnection(hostname, dbname, username, password)
factory = sessionmaker(bind=engine.connect())
session = factory()


@application.route('/', methods=['GET'])
def welcome_endpoint():
    return json.dumps({'message': 'Welcome to LETCO API'})


@application.route('/register', methods=['POST'])
def registration():
    data = json.loads(request.data)
    print(data)
    role = session.get(entity=Role,ident=data['idrole'])
    print(role)
    user = User(name=data['name'], pseudo=data['pseudo'], email=data['email'],
                password=data['password'], bluetooth=data['bluetooth'], idrole=role.id)
    session.add(user)
    session.commit()
    session.flush()
    users = session.query(User).all()
    print(user)
    return application.response_class(response=json.dumps(user, cls=AlchemyEncoder),
                                      status=201, content_type='application/json')


@application.route('/users', methods=['GET'])
def get_all_users():
    users = session.query(User).all()
    print(users)
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
