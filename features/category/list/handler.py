from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.category import Category
from features.category.list.schema import CategoryRequest
from orm import apaging



async def aget_categories(request: CategoryRequest, db: AsyncSession):
    query = select(
        Category.id,
        Category.name,
        Category.parent_id,
        Category.icon,
        Category.status,
        func.exists(select(Category.id).where(Category.parent_id == Category.id).scalar_subquery()).label("has_children")
    )
    if request.name:
        query = query.where(Category.name.ilike(f"%{request.name}%"))
    if request.status:
        query = query.where(Category.status == request.status)
    return await apaging(query=query, page=request, db=db)
