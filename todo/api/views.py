import json

from .. import utils
from .models import Todo, Status
from .schemas import TodoSchema


class TodoHandler(object):

    def __init__(self):
        self.schema = TodoSchema()

    async def get_json(self, request):
        try:
            data = json.loads(await request.text())
        except:
            raise utils.APIException(utils.API_BAD_REQUEST)

        return self.schema.clean(data)

    async def create(self, request):
        data = await self.get_json(request)

        data['user_id'] = int(request.app['userid'])
        data['status'] = Status.ongoing

        rv = await Todo(request.app['db']).create(**data)
        rv = self.schema.to_dict(rv)
        return utils.api_response(payload=rv)

    async def list(self, request):
        status = request.GET.get('status')

        kwargs = {
            "user_id": int(request.app['userid'])
        }
        if status:
            kwargs["status"] = self.schema.clean_status(status)

        rvs = await Todo(request.app['db']).list(**kwargs)
        rvs = self.schema.to_dict(rvs, many=True)

        return utils.api_response(payload={"todos": rvs})

    async def update(self, request):
        todo_id = request.match_info.get('todo_id')

        data = await self.get_json(request)
        data['_filters'] = {
            "id": todo_id,
            "user_id": int(request.app['userid'])
        }

        rv = await Todo(request.app['db']).update(**data)
        if rv == 0:
            raise utils.APIException(utils.API_NOT_FOUND)

        return utils.api_response(payload={"todo_id": todo_id})

    async def delete(self, request):
        todo_id = request.match_info.get('todo_id')
        kwargs = {
            "id": todo_id,
            "user_id": int(request.app['userid'])
        }
        rv = await Todo(request.app['db']).delete(**kwargs)
        if rv == 0:
            raise utils.APIException(utils.API_NOT_FOUND)

        return utils.api_response(payload={"todo_id": todo_id})
