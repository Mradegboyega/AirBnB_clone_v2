#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base


class DBStorage:
    """Database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes DBStorage"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns all objects"""
        obj_dict = {}
        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for cls in [State, City]:
                objs += self.__session.query(cls).all()
        for obj in objs:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Adds the object to the session"""
        self.__session.add(obj)

    def save(self):
        """Saves the session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes the object"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads the session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the session"""
        self.__session.close()
