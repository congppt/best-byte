from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from exception import ValidationError
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in features.routers:
    app.include_router(router, prefix="/api")


@app.exception_handler(ValidationError)
async def validation_exception_handler(_: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": {"message": str(exc), "type": "custom"}},
    )
