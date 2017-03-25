from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.sql import func

from .. import utils
from ..storage import metadata
from ..storage import BaseModel


class Status(object):
    ongoing = 0
    finished = 1


todos = Table(
    'todo',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('content', String(512)),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('status', Integer, default=Status.ongoing)
)


class Todo(object):

    def __init__(self, db):
        self._model = BaseModel(db, todos)

    async def create(self, **kwargs):
        rv = await self._model.create(**kwargs)
        return rv

    async def list(self, **fields):
        rv = await self._model.list(**fields)
        return rv

    async def update(self, todo_id, **fields):
        rv = await self._model.update(todo_id, **fields)
        if not rv:
            raise utils.APIException(utils.API_NOT_FOUND)
        return rv
