from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from features.category.create import handler
from .schema import CreateCategoryRequest
from database import aget_session


async def acreate_category(
    request: CreateCategoryRequest, db: AsyncSession = Depends(aget_session)
):
    category = await handler.acreate_category(request, db)
    return category
