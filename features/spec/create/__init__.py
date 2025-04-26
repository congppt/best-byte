from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from features.spec.create import handler
from features.spec.create.schema import CreateSpecRequest
from database import aget_session


async def acreate_spec(
    request: CreateSpecRequest, db: AsyncSession = Depends(aget_session)
):
    spec = await handler.acreate_spec(request, db)
    return spec
