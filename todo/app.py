import jinja2
import aiohttp_jinja2
from aiohttp import web
from rororo.settings import immutable_settings

from . import settings
from . import middlewares
from .auth import views as auth_views
from .api import views as api_views
from .utils import add_route_context


def get_middleware_list():
    middleware_list = [
        middlewares.db_middleware,
    ]
    return middleware_list


def setup_router(app):
    with add_route_context(app, auth_views, '/auth', 'auth') as add_route:
        add_route('POST', '/register', 'register')
        add_route('POST', '/login', 'login')
        add_route('GET', '/verify-token', 'verify_token')
        add_route('GET', '/refresh-token', 'refresh_token')

    with add_route_context(app, api_views, '/api', 'api') as add_route:
        add_route('GET', '/todos', 'list_todo')
        add_route('POST', '/todos', 'create_todo')
        add_route('DELETE', '/todos/{todo_id:\d+}', 'remove_todo')
        add_route('POST', '/todos/{todo_id:\d}', 'update_todo')

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
