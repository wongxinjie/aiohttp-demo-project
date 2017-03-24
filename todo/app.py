import base64
import logging

import jinja2
import aiohttp_jinja2
from aiohttp import web
from cryptography import fernet
from rororo.settings import immutable_settings
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from . import settings
from . import middlewares
from .auth import views as auth_views
# from .api import views as api_views
# from .utils import add_route_context

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s# %(message)s",
    datefmt="%Y/%m/%d-%H:%M:%S"
)


def gen_secret_key():
    key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(key)
    return secret_key


def get_middleware_list():
    middleware_list = [
        session_middleware(EncryptedCookieStorage(gen_secret_key())),

        middlewares.db_middleware,
        middlewares.authorize,
        middlewares.error_middleware,
    ]
    return middleware_list


def setup_router(app):
    # with add_route_context(app, api_views, '/api', 'api') as add_route:
    #     add_route('GET', '/todos', 'list_todo')
    #     add_route('POST', '/todos', 'create_todo')
    #     add_route('DELETE', '/todos/{todo_id:\d+}', 'remove_todo')
    #     add_route('POST', '/todos/{todo_id:\d}', 'update_todo')
    user_handler = auth_views.UserHandler()
    app.router.add_route(
        'POST', '/auth/register', user_handler.register)
    app.router.add_route(
        'POST', '/auth/login', user_handler.login)
    app.router.add_route(
        'GET', '/auth/logout', user_handler.logout)

    if settings.DEBUG:
        app.router.add_static('/static', settings.STATIC_PATH, name='static')


def load_settings(app, **options):
    settings_dict = immutable_settings(settings, **options)
    app['settings'] = settings_dict


def setup_templates(app):
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(settings.TEMPLATE_PATH)
    )


def create_app():
    app = web.Application(middlewares=get_middleware_list())

    load_settings(app)
    setup_router(app)
    setup_templates(app)
    return app

app = create_app()
