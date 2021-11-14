from aiohttp import web

from models import db, not_found_handler
from view import UserView, AdvView


async def init_orm(app):
    print('start')
    await db.set_bind('postgres://postgres:520911@localhost/aiohttp')
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print('stop')


async def health_check(request: web.Request):
    return web.json_response({'status': 'OK'})


app = web.Application(middlewares=[not_found_handler])
app.add_routes([web.get('/health', health_check)])
app.add_routes([web.post('/user', UserView)])
app.add_routes([web.get('/user/{user_id:\d+}', UserView)])
app.add_routes([web.get('/adv/{adv_id:\d+}', AdvView)])
app.add_routes([web.delete('/adv/{adv_id:\d+}', AdvView)])
app.add_routes([web.patch('/adv/{adv_id:\d+}', AdvView)])
app.add_routes([web.post('/adv', AdvView)])
app.cleanup_ctx.append(init_orm)

if __name__ == '__main__':
    web.run_app(app, port=8080)
