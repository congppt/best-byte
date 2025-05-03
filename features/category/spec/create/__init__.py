from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database import aget_session
from features.category.spec.create.schema import CreateSpecRequest
from features.category.spec.create import handler


async def acreate_spec(
    category_id: Annotated[int, Path(gt=0)],
    request: CreateSpecRequest,
    db: AsyncSession = Depends(aget_session),
):
    spec = await handler.acreate_spec(category_id, request, db)
    return spec
