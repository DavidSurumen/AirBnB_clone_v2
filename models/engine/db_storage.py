#!/usr/bin/python3
"""Database storage engine"""
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Database storage class."""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization."""
        conn = 'mysql+mysqldb://{}:{}@{}:3306/{}'.\
               format(getenv('HBNB_MYSQL_USER'),
                      getenv('HBNB_MYSQL_PWD'),
                      getenv('HBNB_MYSQL_HOST'),
                      getenv('HBNB_MYSQL_DB'))

        self.__engine = create_engine(conn, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries the current database session for all objects."""
        if cls is None:
            objs_list = self.__session.query(User).all()

            objs_list.extend(self.__session.query(State).all())
            objs_list.extend(self.__session.query(City).all())
            objs_list.extend(self.__session.query(Place).all())
            objs_list.extend(self.__session.query(Review).all())
        else:
            objs_list = self.__session.query(cls)

        return {'{}.{}'.format(type(obj).__name__, obj.id): obj
                for obj in objs_list}

    def new(self, obj):
        """Add objects to the current database session."""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database."""
        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Session)

        self.__session = Session()

    def close(self):
        """close session."""
        self.__session.remove()
