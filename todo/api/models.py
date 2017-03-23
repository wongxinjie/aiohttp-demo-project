import enum
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.sql import func

from ..storage import metadata


class Status(enum.Enum):
    ongoing = 0
    finished = 1


todos = Table(
    'todo',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('auth.models.users')),
    Column('content', String(512)),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('status', Status, default=Status.ongoing)
)
