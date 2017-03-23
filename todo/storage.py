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

    async def list(self, **filters):
        async with self._db.acquire() as conn:
            rvs = await conn.execute(
                self._table.select().where(**filters))
            entities = list(map(dict, rvs))
        return entities

    async def create(self, **data):
        async with self._db.acquire() as conn:
            query = self.table.insert().values(
                **data).returning(*self._table.c)

            rv = await conn.execute(query)
            row = await rv.first(0)
            await conn.execute('commit;')
        entity = dict(row)
        return entity

    async def update(self, entity_id, **fields):
        async with self._db.acquire() as conn:
            rv = await conn.execute(
                self._table.update().values(
                    **fields).where(
                    self._table.c.id == entity_id)
            )
        return rv.rowcount

    async def delete(self, entity_id):
        async with self._db.acquire() as conn:
            rv = await conn.execute(
                self._table.delete().where(
                    self._table.c.id == entity_id
                )
            )

        return rv.rowcount

    async def get(self, **fields):
        async with self._db.acquire() as conn:
            query = await conn.execute(
                self._table.select().where(**fields)
            )
            rv = await query.first()

        return rv
