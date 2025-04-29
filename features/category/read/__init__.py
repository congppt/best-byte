from typing import Annotated
from fastapi import Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from features.category.read import handler
from database import aget_session
from features.category.read.schema import CategoryRequest


async def aget_categories(
    request: Annotated[CategoryRequest, Query()],
    db: AsyncSession = Depends(aget_session),
):
    categories = await handler.aget_categories(request, db)
    return categories


async def aget_category_children(
    id: Annotated[int, Path(gt=0)],
    request: Annotated[CategoryRequest, Query()],
    db: AsyncSession = Depends(aget_session),
):
    categories = await handler.aget_category_children(id, request, db)
    return categories
