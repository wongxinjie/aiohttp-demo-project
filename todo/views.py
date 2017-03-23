from aiohttp_jinja2 import render_template

from .storage import users_table
from .utils import (
    api_response,
    redirect
)


async def search(request):
    query = request.GET.get('query', '')
    payload = {
        "query": query
    }
    return api_response(payload=payload)


async def project(request):
    project_id = request.match_info['project_id']
    payload = {
        "current_project_id": project_id
    }
    return api_response(payload=payload)


async def projects(request):
    payload = {
        "project_count": 10
    }
    return api_response(payload=payload)


async def add_project(request):
    data = await request.post()
    print(data['title'], type(data['title']))
    url = request.app.router['projects'].url()
    return redirect(url)


async def index(request):
    return render_template('index.html', request, {"text": "message"})


async def add_user(request):
    data = await request.post()
    email, password = data['email'], data['password']
    async with request.app['db'].acquire() as conn:
        await conn.execute(users_table.insert().values(
            email=email, password=password))
        await conn.execute('commit')

    url = request.app.router['users'].url()
    return redirect(url)


async def users(request):
    payload = {'users': []}
    async with request.app['db'].acquire() as conn:
        rvs = await conn.execute(users_table.select())
        for rv in rvs:
            payload['users'].append(
                {'id': rv.id, 'email': rv.email})

    print(payload)
    return api_response(payload=payload)
