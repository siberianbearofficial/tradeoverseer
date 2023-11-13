from random import randint

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from utils.config import REDIS_HOST, REDIS_PORT, REDIS_HOST_TEST

from authentication.router import router as authentication_router
from users.router import router as users_router
from records.router import router as records_router
from skins.router import router as skins_router
from inventory.router import router as inventory_router
from roles.router import router as roles_router
from rarities.router import router as rarities_router
from orders.router import router as orders_router

app = FastAPI(
    title='TradeOverseer'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/static', StaticFiles(directory='/static'), name='static')


@app.get(f'/ping', tags=['Setup'])
@cache(namespace='test')
async def get_ping_handler():
    return {
        'data': None,
        'details': f'HTTP {randint(200, 300)} OK'
    }


@app.get('/clear', tags=['Setup'])
async def get_clear_handler():
    await FastAPICache.clear('test')
    return {
        'data': None,
        'details': 'Cache cleared.'
    }


app.include_router(authentication_router)
app.include_router(users_router)
app.include_router(records_router)
app.include_router(skins_router)
app.include_router(inventory_router)
app.include_router(roles_router)
app.include_router(rarities_router)
app.include_router(orders_router)


@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', encoding='utf8', decode_responses=False)  # TODO change host when run in docker
    FastAPICache.init(RedisBackend(redis), prefix='tradeoverseer-backend-cache')
