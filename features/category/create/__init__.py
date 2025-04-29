from typing import Annotated
from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from features.category.create import handler
from .schema import CreateCategoryRequest, CreateSpecRequest
from database import aget_session


async def acreate_category(
    request: CreateCategoryRequest, db: AsyncSession = Depends(aget_session)
):
    category = await handler.acreate_category(request, db)
    return category


async def acreate_spec(
    category_id: Annotated[int, Path(gt=0)],
    request: CreateSpecRequest,
    db: AsyncSession = Depends(aget_session),
):
    spec = await handler.acreate_spec(category_id, request, db)
    return spec
