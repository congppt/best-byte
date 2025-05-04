from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models.category import Spec, SpecComparison
from features.spec.read.schema import SpecComparisonResponse, SpecRequest
from orm import apaging


async def aget_specs(request: SpecRequest, db: AsyncSession):
    query = select(
        Spec.id,
        Spec.category_id,
        Spec.label,
        Spec.type,
        Spec.units,
        Spec.filterable,
        func.exists(
            select(1)
            .where(
                (SpecComparison.left_id == Spec.id)
                | (SpecComparison.right_id == Spec.id)
            )
            .scalar_subquery()
        ).label("has_comparisons"),
    ).where(Spec.category_id == request.category_id)
    if request.label:
        query = query.where(Spec.label.ilike(f"%{request.label}%"))
    return await apaging(query=query, page=request, db=db)


async def aget_spec_comparisons(id: int, db: AsyncSession):
    query = (
        select(SpecComparison)
        .where((SpecComparison.left_id == id) | (SpecComparison.right_id == id))
        .options(
            joinedload(SpecComparison.left).joinedload(Spec.category),
            joinedload(SpecComparison.right).joinedload(Spec.category),
        )
    )
    comparisons = (await db.scalars(query)).all()
    result: list[SpecComparisonResponse] = []
    for comparison in comparisons:
        is_left = comparison.left_id == id
        result.append(
            SpecComparisonResponse(
                spec_id=comparison.right_id if is_left else comparison.left_id,
                label=comparison.right.label if is_left else comparison.left.label,
                category={comparison.right.category.id: comparison.right.category.name}
                if is_left
                else {comparison.left.category.id: comparison.left.category.name},
                operator=comparison.operator if is_left else comparison.operator.flip(),
            )
        )
    return result
