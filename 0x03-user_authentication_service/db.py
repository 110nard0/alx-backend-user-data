#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from typing import Dict

from user import Base, User


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create User instance object and save to database
        Args:
            email (str): user's email address
            hashed_password (str): user's password hashed by bcrypt's hashpw
        Return:
            (User): Newly created User class instance
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Search for user with attribute(s) matching keyword argument(s)
        Args:
            attributes (dict): a dictionary of attributes to match user
        Return:
            Matching user or raised error if user not found
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except AttributeError:
            raise InvalidRequestError


    def update_user(self, user_id: int, **kwargs) -> None:
        """Update found user's attributes
        Args:
            user_id (int): user's id
            kwargs (dict): dictionary of key:value pairs representing the
                           attributes to update and their corresponding values
        Return:
            None
        """
        try:
            user = self._session.query(User).filter(User.id == int(user_id))
            if user is None:
                raise NoResultFound
            for k, v in kwargs.items():
                if k not in User.__dict__:
                    raise InvalidRequestError
                for key in user.__dict__:
                    if k == key:
                        setattr(user, k, v)
        except ValueError:
            raise






"""
In this task, you will implement the DB.update_user method that takes
as argument a required user_id integer and arbitrary keyword arguments,
and returns None.

The method will use find_user_by to locate the user to update,
then will update the user’s attributes as passed in the method’s arguments
then commit changes to the database.

If an argument that does not correspond to a user attribute is passed,
raise a ValueError.
"""
