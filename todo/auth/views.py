import json

from aiohttp_session import get_session

from .. import utils
from .models import User
from .schemas import UserSchema


class UserHandler(object):

    def __init__(self):
        self.schema = UserSchema()

    async def get_json(self, request):
        try:
            data = json.loads(await request.text())
        except:
            raise utils.APIException(utils.API_BAD_REQUEST)

        return self.schema.clean(data)

    async def login(self, request):
        data = await self.get_json(request)

        rv = await User(request.app['db']).get(**data)
        rv = self.schema.to_dict(rv)

        session = await get_session(request)
        session["user"] = rv['id']
        return utils.api_response(payload=rv)

    async def register(self, request):
        data = await self.get_json(request)

        rv = await User(request.app['db']).create(**data)
        rv = self.schema.to_dict(rv)
        return utils.api_response(payload=rv)

    async def logout(self, request):
        session = await get_session(request)
        del session["user"]
        return utils.api_response(message="logout success!")
