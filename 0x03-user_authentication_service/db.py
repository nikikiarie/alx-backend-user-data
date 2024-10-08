#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

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
        """Adds a new user to the database.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """searches for user by kwargs
        """
        a, b = [], []
        for i, j in kwargs.items():
            if hasattr(User, i):
                a.append(getattr(User, i))
                b.append(j)
            else:
                raise InvalidRequestError()
        res = self._session.query(User).filter(
            tuple_(*a).in_([tuple(b)])
        ).first()
        if res is None:
            raise NoResultFound()
        return res

    def update_user(self, user_id: int, *args, **kwargs) -> None:
        """ updates user """
        arr = [
            'email',
            'id',
            'hashed_password',
            'session_id',
            'reset_token'
            ]
        user = self.find_user_by(id=user_id)
        for i in kwargs:
            if i not in arr:
                raise ValueError
            user.__setattr__(i, kwargs[i])
        self._session.commit()
