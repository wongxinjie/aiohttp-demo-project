from aiomysql.sa import create_engine


async def db_middleware(app, handler):

    async def middleware(request):
        db = app.get('db')
        if not db:
            db_conf = app['settings']['DATABASE']
            app['db'] = db = await create_engine(
                user=db_conf['USERNAME'],
                db=db_conf['DATABASE'],
                host=db_conf['HOST'],
                password=db_conf['PASSWORD']
            )

        request.app['db'] = db

        return await handler(request)

    return middleware
