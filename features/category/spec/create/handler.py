from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.category import Category, Spec
from exception import ValidationError
from features.category.spec.create.schema import CreateSpecRequest


async def aget_category(id: int, db: AsyncSession):
    query = select(Category).where(Category.id == id)
    category = await db.scalar(query)
    return category


async def acreate_spec(category_id: int, request: CreateSpecRequest, db: AsyncSession):
    category = await aget_category(category_id, db)
    if not category:
        raise ValidationError("Category is not existed")
    if not category.parent_id:
        raise ValidationError("Top level category cannot have specs")
    # Check spec name is used
    used_label_query = select(
        exists(select(1)).where(
            Spec.category_id == category_id, Spec.label == request.label
        )
    )
    used_label = await db.scalar(used_label_query)
    if used_label:
        raise ValidationError(
            f"{category.name} already has {request.label} specification"
        )
    spec = Spec.from_dict(**request.model_dump(), category_id=category_id)
    db.add(spec)
    await db.commit()
    return spec
