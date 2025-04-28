from sqlalchemy import select
from database.models.category import Category
from exception import ValidationError
from features.category.create.schema import CreateCategoryRequest
from sqlalchemy.ext.asyncio import AsyncSession


async def aget_existed_category(id: int, db: AsyncSession):
    query = select(Category).where(Category.id == id)
    category = await db.scalar(query)
    return category


async def acreate_category(request: CreateCategoryRequest, db: AsyncSession):
    # Check category name is used
    used_name_query = select(Category).where(Category.name == request.name)
    used_name = await db.scalar(used_name_query)
    if used_name:
        raise ValidationError("Category name is already used")
    # Check parent category is existed
    if request.parent_id and not await aget_existed_category(request.parent_id, db):
        raise ValidationError("Parent category is not existed")
    category = Category(**request.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category
