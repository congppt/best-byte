from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from features.category.create import handler
from database import aget_session


async def aget_categories(
    db: AsyncSession = Depends(aget_session)
):
    pass
