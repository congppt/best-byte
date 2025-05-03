from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.category import Spec, SpecComparison
from features.spec.read.schema import SpecRequest
from orm import apaging


async def aget_specs(request: SpecRequest, db: AsyncSession):
    query = select(
        Spec.id,
        Spec.category_id,
        Spec.label,
        Spec.type,
        Spec.units,
        Spec.filterable,
        func.exists(select(1).where((SpecComparison.left_id == Spec.id) | (SpecComparison.right_id == Spec.id)).scalar_subquery()).label("has_comparisons"),
    ).where(Spec.category_id == request.category_id)
    if request.label:
        query = query.where(Spec.label.ilike(f"%{request.label}%"))
    return await apaging(query=query, page=request, db=db)
