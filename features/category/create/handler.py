from sqlalchemy import exists, select
from database.models.category import Category
from database.models.enum import CategoryStatus
from exception import ValidationError
from features.category.create.schema import CreateCategoryRequest
from sqlalchemy.ext.asyncio import AsyncSession


async def acreate_category(request: CreateCategoryRequest, db: AsyncSession):
    # Check parent category is existed
    if request.parent_id:
        parent_existed_query = select(
            exists(
                select(1).where(
                    Category.id == request.parent_id,
                    Category.status.in_({CategoryStatus.ACTIVE}),
                )
            )
        )
        if not await db.scalar(parent_existed_query):
            raise ValidationError("Parent category is not existed")
    # Check category name is used
    used_name_query = select(exists(select(1).where(Category.name == request.name)))
    used_name = await db.scalar(used_name_query)
    if used_name:
        raise ValidationError("Category name is already used")

    category = Category.from_dict(**request.model_dump())
    db.add(category)
    await db.commit()
    return category
