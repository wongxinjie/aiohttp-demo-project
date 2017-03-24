from aiohttp import web

from aiomysql.sa import create_engine
from aiohttp_session import get_session

from . import utils


async def db_middleware(app, handler):

    async def middleware(request):
        db = app.get('db')
        if not db:
            db_conf = app['settings']['DATABASE']
            app['db'] = db = await create_engine(
                user=db_conf['USERNAME'],
                db=db_conf['DB'],
                host=db_conf['HOST'],
                password=db_conf['PASSWORD']
            )

        request.app['db'] = db

        return await handler(request)

    return middleware


async def authorize(app, handler):

    async def middleware(request):

        def check_auth(path):
            freeuris = ['/auth/register', '/auth/login']
            for r in freeuris:
                if path.startswith(r):
                    return False
            return True

        session = await get_session(request)
        if session.get("user"):
            return await handler(request)

        if check_auth(request.path):
            return web.json_response(
                utils.APIException(utils.API_UNAUTHENTICATED).to_dict())

        return await handler(request)

    return middleware


async def error_middleware(app, handler):

    async def middleware(request):
        try:
            return await handler(request)
        except utils.APIException as err:
            return web.json_response(err.to_dict())

    return middleware
