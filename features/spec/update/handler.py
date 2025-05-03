from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.category import SpecComparison
from database.models.enum import SpecComparisonOperator


async def aupdate_comparisons(id: int, comparisons: dict[int, SpecComparisonOperator | None], db: AsyncSession):
    comparisons_query = select(SpecComparison).where((SpecComparison.left_id == id) | (SpecComparison.right_id == id))
    current_comparisons = (await db.execute(comparisons_query)).mappings().all()
    for spec_id, operator in comparisons.items():
        if spec_id in current_comparisons:
            if operator is None:
                await db.delete(current_comparisons[spec_id])
            else:
                current_comparisons[spec_id].operator = operator
        else:
            current_comparison = SpecComparison(left_id=id, right_id=spec_id, operator=operator)
            db.add(current_comparison)

    await db.commit()
    return