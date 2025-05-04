from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import aget_session
from features.spec.create.schema import CreateSpecRequest
from features.spec.create import handler


async def acreate_spec(
    request: CreateSpecRequest,
    db: AsyncSession = Depends(aget_session),
):
    spec = await handler.acreate_spec(request, db)
    return spec
