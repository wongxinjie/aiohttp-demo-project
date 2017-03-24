from pymysql.err import IntegrityError
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String
)

from .. import utils
from ..storage import metadata
from ..storage import BaseModel

users = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(128), unique=True),
    Column('password', String(64))
)


class User(object):

    def __init__(self, db):
        self._model = BaseModel(db, users)

    async def create(self, **kwargs):
        """add user, #TODO encrypt password
        Args:
            kwargs: {'email': '', 'password': ''}
        Return:
            {'id': '', 'email': '', 'password': ''}
        Raise:
            APIException
        """

        try:
            rv = await self._model.create(**kwargs)
        except IntegrityError:
            raise utils.APIException(
                utils.API_DUPLICATE, name="email")
        return rv

    async def get(self, email, password):
        """
        Args:
            email: user email
            password: user password
        Return:
            {"id": "", "email": "", "password": ""}
        Raise:
            APIException
        """
        rv = await self._model.get(email=email, password=password)
        if not rv:
            raise utils.APIException(
                utils.API_NOT_FOUND,
                message="用户未注册或密码不正确"
            )
        return rv
