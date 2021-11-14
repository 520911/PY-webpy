import hashlib

import pydantic
from aiohttp import web

from models import NotFound, User, Adv


class LoginUserSerializer(pydantic.BaseModel):
    username: str
    password: str


async def login(request: web.Request):
    login_data = await request.json()
    login_data_serializer = LoginUserSerializer(**login_data).dict()
    return login_data_serializer


class UserView(web.View):

    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await User.get(user_id)
        if user is None:
            raise NotFound
        return web.json_response(user.to_dict())

    async def post(self):
        user_data = await self.request.json()
        user_data['password'] = hashlib.md5(user_data['password'].encode()).hexdigest()
        new_user = await User.create(**user_data)
        return web.json_response(new_user.to_dict())


class AdvView(web.View):

    async def get(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await Adv.get(adv_id)
        if adv is None:
            raise NotFound
        return web.json_response(adv.to_dict())

    async def post(self):
        adv_data = await self.request.json()
        user_id = int(adv_data.get('user_id'))
        user = await User.get(user_id)
        if user is not None:
            new_adv = await Adv.create(**adv_data)
            response = new_adv.to_dict()
            return web.json_response(response)
        else:
            return web.json_response({'errors': 'Not user'})

    async def delete(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await Adv.get(adv_id)
        if adv is None:
            raise NotFound
        else:
            await adv.delete()
        return web.json_response({'Adv': 'Adv delete'})

    async def patch(self):
        new_adv = await self.request.json()
        adv_id = int(self.request.match_info['adv_id'])
        adv = await Adv.get(adv_id)
        if adv is None:
            raise NotFound
        else:
            await adv.update(title=new_adv.get('title')).apply()
            await adv.update(content=new_adv.get('content')).apply()
        return web.json_response({'Adv': 'Adv patched'})
