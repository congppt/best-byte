import math
from typing import TypeVar
from sqlalchemy import Select, func, select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession

from utils.schema import PageRequest, PageResponse

T = TypeVar("T", bound=DeclarativeBase)


async def apaging(query: Select[tuple], page: PageRequest, db: AsyncSession):
    """
    Executes given query and return paging result.
    ``query`` parameter should not be chained with ``limit()`` and ``offset()`` to avoid wrong counting.
    """
    count_query = select(func.count()).select_from(query.subquery())
    count = await db.scalar(statement=count_query)
    if count is None:
        raise ValueError("Count query returned no result")
    total_pages = math.ceil(count / page.size)
    page_query = query.offset(offset=page.index * page.size).limit(limit=page.size)
    if len(query.column_descriptions) == 1:
        items = (await db.execute(statement=page_query)).scalars().all()
    else:
        items = (await db.execute(statement=page_query)).mappings().all()
    return PageResponse(items=items, total_pages=total_pages, total_items=count)
