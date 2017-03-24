from contextlib import contextmanager

from aiohttp import web


API_CODE_OK = 200
API_DUPLICATE = 204
API_REQUIRED = 400
API_BAD_REQUEST = 400
API_UNAUTHENTICATED = 401
API_FORBIDDEN = 403
API_NOT_FOUND = 404

ARGUMENT_NAME = {
    "username":  "用户名",
    "email": "邮箱",
    "passowrd": "密码",
    "content": "内容",
}


API_CODE_MESSAGE = {
    API_CODE_OK: "OK",
    API_BAD_REQUEST: "请求数据格式错误",
    API_REQUIRED: "参数错误",
    API_UNAUTHENTICATED: "用户没有登录",
    API_FORBIDDEN: "用户没有权限",
    API_NOT_FOUND: "Entity不存在",
    API_DUPLICATE: "{name}已存在"
}


class APIResponse():

    def __init__(self, status_code=None, message=None, payload=None, **kwargs):
        if 'name' in kwargs and kwargs['name'] in ARGUMENT_NAME:
            kwargs['name'] = ARGUMENT_NAME[kwargs['name']]

        self.status_code = status_code or API_CODE_OK
        self.message = message or API_CODE_MESSAGE[self.status_code]
        self.message = self.message.format(**kwargs)
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())

        if self.message is not None:
            rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


class APIException(Exception, APIResponse):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self)
        APIResponse.__init__(self, *args, **kwargs)


def api_response(*args, **kwargs):
    return web.json_response(APIResponse(*args, **kwargs).to_dict())


def redirect(url, *args, **kwargs):
    return web.HTTPFound(url)


@contextmanager
def add_route_context(app, views, url_prefix=None, name_prefix=None):
    def add_route(method, url, name):
        view = getattr(views, name)

        if url_prefix is not None:
            url = '/'.join([url_prefix.rstrip('/'), url])
        if name_prefix is not None:
            name = '.'.join(name_prefix, name)

        return app.router.add_route(method, url, view, name=name)

    return add_route
