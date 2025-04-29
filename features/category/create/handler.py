from sqlalchemy import select
from database.models.category import Category, Spec, SpecComparision
from database.models.enum import SpecStatus
from exception import ValidationError
from features.category.create.schema import CreateCategoryRequest, CreateSpecRequest
from sqlalchemy.ext.asyncio import AsyncSession


async def aget_category(id: int, db: AsyncSession):
    query = select(Category).where(Category.id == id)
    category = await db.scalar(query)
    return category


async def acreate_category(request: CreateCategoryRequest, db: AsyncSession):
    # Check parent category is existed
    if request.parent_id and not await aget_category(request.parent_id, db):
        raise ValidationError("Parent category is not existed")
    # Check category name is used
    used_name_query = select(Category).where(Category.name == request.name)
    used_name = await db.scalar(used_name_query)
    if used_name:
        raise ValidationError("Category name is already used")
    
    category = Category.from_dict(**request.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def acreate_spec(category_id: int, request: CreateSpecRequest, db: AsyncSession):
    category = await aget_category(category_id, db)
    if not category:
        raise ValidationError("Category is not existed")
    if not category.parent_id:
        raise ValidationError("Top level category cannot have specs")
    spec = Spec.from_dict(**request.model_dump(), category_id=category_id)
    db.add(spec)
    if request.comparisions:
        compared_spec_ids = request.comparisions.keys()
        compare_query = select(Spec).where(
            Spec.id.in_(compared_spec_ids), Spec.status == SpecStatus.ACTIVE
        )
        compared_specs = (await db.scalars(compare_query)).all()
        if len(compared_specs) != len(compared_spec_ids):
            raise ValidationError(
                "Some compared spec is not existed/active: "
                + ", ".join(
                    str(id)
                    for id in compared_spec_ids - {spec.id for spec in compared_specs}
                )
            )
        spec_comparisions = []
        for compared_spec in compared_specs:
            if compared_spec.type != request.type:
                raise ValidationError("Compared spec type is not matched")
            if compared_spec.units - request.units:
                raise ValidationError("Compared spec units are not fully matched")
            spec_comparisions.append(
                SpecComparision(
                    left=spec,
                    right_id=compared_spec.id,
                    operator=request.comparisions[compared_spec.id],
                )
            )
        db.add_all(spec_comparisions)
    await db.commit()
    await db.refresh(spec)
    return spec
