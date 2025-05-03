from typing import Annotated

from fastapi import Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import aget_session
from features.spec.read import handler
from features.spec.read.schema import SpecRequest


async def aget_specs(request: Annotated[SpecRequest, Query()], db: AsyncSession = Depends(aget_session)):
    specs = await handler.aget_specs(request, db)
    return specs
