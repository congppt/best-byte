from typing import Annotated

from fastapi import Path, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import aget_session
from features.spec.read import handler
from features.spec.read.schema import SpecRequest


async def aget_specs(
    request: Annotated[SpecRequest, Query()], db: AsyncSession = Depends(aget_session)
):
    specs = await handler.aget_specs(request, db)
    return specs


async def aget_spec_comparisons(
    id: Annotated[int, Path(gt=0)], db: AsyncSession = Depends(aget_session)
):
    comparisons = await handler.aget_spec_comparisons(id, db)
    return comparisons
