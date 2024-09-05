import aioredis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

async def init_limiter(app: FastAPI):
    redis = await aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)  # Redis host is 'redis' in docker-compose
    await FastAPILimiter.init(redis)
