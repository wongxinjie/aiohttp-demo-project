from copy import deepcopy
from collections import namedtuple

import sqlalchemy as sa
from sqlalchemy import create_engine

from . import settings

metadata = sa.MetaData()


def create_tables():
    import pymysql
    pymysql.install_as_MySQLdb()

    db_conf = settings.DATABASE
    engine = create_engine(
        'mysql+mysqldb://{user}:{password}@{host}/{db}'.format(
            user=db_conf['USERNAME'],
            password=db_conf['PASSWORD'],
            host=db_conf['HOST'],
            db=db_conf['DB']
        )
    )
    metadata.create_all(engine)


PagingParams = namedtuple(
    'PagingParams', ['limit', 'offset', 'sorted_field', 'sort_dir'])


class BaseModel(object):

    def __init__(self, db, table):
        self._db = db
        self._table = table

    def create_filters(self, query, filters):
        for field, value in filters.items():
            query = query.where(
                getattr(self._table.c, field) == value
            )
        return query

    async def list(self, **filters):
        async with self._db.acquire() as conn:
            query = self._table.select()

            query = self.create_filters(query, filters)
            rvs = await conn.execute(query)

            entities = list(map(dict, rvs))
        return entities

    async def create(self, **data):
        async with self._db.acquire() as conn:
            query = self._table.insert().values(**data)
            rv = await conn.execute(query)
            await conn.execute('commit;')
        entity = deepcopy(data)
        entity.update({"id": rv.lastrowid})
        return entity

    async def update(self, **fields):
        filters = fields.pop('_filters')

        async with self._db.acquire() as conn:
            query = self._table.update().vaues(**fields)
            query = self.create_filters(query, filters)

            rv = await conn.execute(query)
            await conn.execute('commit;')

        return rv.rowcount

    async def delete(self, **filters):
        async with self._db.acquire() as conn:
            query = self._table.delete()
            query = self.create_filters(query, filters)

            rv = await conn.execute(query)
            await conn.execute('commit;')

        return rv.rowcount

    async def get(self, **filters):
        async with self._db.acquire() as conn:
            query = self._table.select()
            query = self.create_filters(query, filters)

            rv = await conn.execute(query)
            rv = await rv.first()
        return rv
