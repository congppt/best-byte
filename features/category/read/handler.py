from sqlalchemy import func, select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.category import Category
from exception import NotFoundException
from features.category.read.schema import CategoryRequest
from orm import apaging


SubCategory = aliased(Category, name="sub_category")


async def aget_categories(request: CategoryRequest, db: AsyncSession):
    query = select(
        Category.id,
        Category.name,
        Category.parent_id,
        Category.icon,
        Category.status,
        func.exists(
            select(SubCategory.id)
            .where(SubCategory.parent_id == Category.id)
            .scalar_subquery()
        ).label("has_children"),
    ).where(Category.parent_id.is_(None))
    if request.name:
        query = query.where(Category.name.ilike(f"%{request.name}%"))
    if request.status:
        query = query.where(Category.status == request.status)
    return await apaging(query=query, page=request, db=db)


async def aget_category_children(id: int, request: CategoryRequest, db: AsyncSession):
    # Check if category exists
    exist_query = select(Category.id).where(Category.id == id)
    category_exist = await db.scalar(exist_query)
    if not category_exist:
        raise NotFoundException("Category does not exist")

    # Get children with pagination
    query = select(
        Category.id,
        Category.name,
        Category.parent_id,
        Category.icon,
        Category.status,
        func.exists(
            select(SubCategory.id)
            .where(SubCategory.parent_id == Category.id)
            .scalar_subquery()
        ).label("has_children"),
    ).where(Category.parent_id == id)

    if request.name:
        query = query.where(Category.name.ilike(f"%{request.name}%"))
    if request.status:
        query = query.where(Category.status == request.status)

    return await apaging(query=query, page=request, db=db)
