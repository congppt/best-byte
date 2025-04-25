from datetime import timedelta
import json
from typing import TypeVar, Any
from redis.asyncio import Redis
from pydantic import BaseModel
from pydantic_core import from_json, to_jsonable_python
from constants import CACHE_URL


__cache = Redis.from_url(CACHE_URL)
T = TypeVar("T")


async def aget(key: str, klass: type[T] | None = None) -> T | Any | None:
    """
    Get object from cache
    :param key: key used to store object
    :param model: type of object
    :return: deserialized object
    """
    value = await __cache.get(name=key)
    if value:
        obj = from_json(data=value)
        if not klass:
            return obj
        if issubclass(klass, BaseModel):
            return klass.model_validate(obj)
        return klass.__init__(obj)
    return None


async def aset(key: str, value: Any, expire: int | timedelta | None = None):
    """
    Store object in cache
    :param key: key used to store
    :param value: object to store
    :param expire: object expired after ``expire`` seconds
    """
    value = json.dumps(to_jsonable_python(value))
    await __cache.set(name=key, value=value, ex=expire)
