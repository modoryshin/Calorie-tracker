from contextlib import contextmanager
from fastapi import FastAPI
from redis import Redis

async def lifespan(app: FastAPI):
    app.state.redis = Redis(host='localhost', port=6379)
    yield
    app.state.redis.close()