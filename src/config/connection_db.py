from sqlalchemy import create_engine


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class DbConnection:
    def __init__(self, hostname, dbname, username, password):
        self.hostname = hostname
        self.dbname = dbname
        self.username = username
        self.password = password

    def connect(self):
        try:
            engine = create_engine('postgresql+psycopg2://' + self.username + ':' +
                                   self.password + '@' + self.hostname + '/' +
                                   self.dbname)
            return engine
        except Exception as ex:
            print(f'Sorry failed to connect: {ex}')
            return ex
