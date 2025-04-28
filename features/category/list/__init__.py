from typing import Annotated
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from features.category.list import handler
from database import aget_session
from features.category.list.schema import CategoryRequest



async def aget_categories(
    request: Annotated[CategoryRequest, Query()], db: AsyncSession = Depends(aget_session)
):
    categories = await handler.aget_categories(request, db)
    return categories
