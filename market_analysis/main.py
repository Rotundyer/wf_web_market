import uvicorn
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis_settings import redis_client
from market_analysis.db.session import sessionmanager
from settings import REAL_DATABASE_URL, API_HOST, API_PORT
from routers.web_page import router as router_web
from routers.admin_page import router as router_admin
from routers.api_handler import router as router_api
from backstage.backstage import BackstageRunner


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(RedisBackend(redis_client), prefix='fastapi-cache')

    sessionmanager.init(REAL_DATABASE_URL)

    backstage = BackstageRunner()
    asyncio.create_task(backstage.update_orders())

    yield


app = FastAPI(title='TadeWARF', lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router_web)
app.include_router(router_admin)
app.include_router(router_api)

if __name__ == '__main__':
    uvicorn.run(app, host=API_HOST, port=API_PORT)
