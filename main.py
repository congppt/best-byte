from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import features


async def astartup():
    pass


async def ashutdown():
    pass


@asynccontextmanager
async def lifespan(_: FastAPI):
    await astartup()
    yield
    await ashutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in features.routers:
    app.include_router(router, prefix="/api")
