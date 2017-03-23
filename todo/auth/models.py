from sqlalchemy import (
    Table,
    Column,
    Integer,
    String
)

from ..storage import metadata

users = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(128), unique=True),
    Column('password', String(64))
)
