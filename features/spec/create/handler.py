from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.category import Category
from database.models.spec import Spec
from exception import ValidationError
from features.spec.create.schema import CreateSpecRequest
from database import aget_session

async def aget_existed_category(id: int, db: AsyncSession):
    query = select(Category).where(Category.id == id)
    category = await db.scalar(query)
    return category

async def acreate_spec(request: CreateSpecRequest, db: AsyncSession = Depends(aget_session)):
    # Check category is existed
    if await aget_existed_category(request.category_id, db):
        raise ValidationError("Danh mục không tồn tại")
    spec = Spec(**request.model_dump())
    db.add(spec)
    await db.commit()
    await db.refresh(spec)
    return spec