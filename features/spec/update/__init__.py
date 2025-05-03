from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database import aget_session
from database.models.enum import SpecComparisonOperator
from features.spec.update import handler


async def aupdate_comparisons(id: Annotated[int, Path(gt=0)], comparisons: dict[int, SpecComparisonOperator | None], db: AsyncSession = Depends(aget_session)):
    spec = await handler.aupdate_comparisons(id, comparisons, db)
    return spec
