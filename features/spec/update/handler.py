from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.category import Spec, SpecComparison
from database.models.enum import SpecComparisonOperator
from exception import ValidationError


async def aupdate_comparisons(
    id: int, comparisons: dict[int, SpecComparisonOperator | None], db: AsyncSession
):
    if id in comparisons:
        raise ValidationError("Cannot compare spec to itself")
    comparisons_query = select(SpecComparison).where(
        (SpecComparison.left_id == id) | (SpecComparison.right_id == id)
    )
    # update existing comparisons
    existing_comparisons = {
        comparison.right_id
        if comparison.left_id == id
        else comparison.left_id: comparison
        for comparison in (await db.execute(comparisons_query)).scalars().all()
    }
    new_compared_specs = {id}
    for spec_id, operator in comparisons.items():
        if spec_id in existing_comparisons:
            if operator is None:
                await db.delete(existing_comparisons[spec_id])
            else:
                # flip operator if main spec is on the right side of operation
                existing_comparisons[spec_id].operator = (
                    operator
                    if existing_comparisons[spec_id].left_id == id
                    else operator.flip()
                )
        else:
            new_compared_specs.add(spec_id)
    # add new comparisons
    specs_query = select(Spec).where(Spec.id.in_(new_compared_specs))
    specs = (await db.scalars(specs_query)).all()
    if len(specs) != len(new_compared_specs):
        raise ValidationError(
            "Unknown specs: "
            + ", ".join(
                str(spec_id)
                for spec_id in new_compared_specs - set(spec.id for spec in specs)
            )
        )
    left_spec = next((spec for spec in specs if spec.id == id), None)
    if not left_spec:
        raise ValidationError("Unknown spec: " + str(id))
    # new_comparisons: set[SpecComparison] = set()
    for right_spec in specs:
        if right_spec.id == id:
            continue
        operator = comparisons.get(right_spec.id)
        if operator is None:
            continue
        if right_spec.type != left_spec.type:
            raise ValidationError(
                f"Cannot compare specs of different types: {left_spec.label}({left_spec.type}) and {right_spec.label}({right_spec.type})"
            )
        if right_spec.units != left_spec.units:
            raise ValidationError(
                f"Cannot compare specs with different units: {left_spec.label}({left_spec.units}) and {right_spec.label}({right_spec.units})"
            )
        if operator not in left_spec.type.supported_operators:
            raise ValidationError(
                f"{left_spec.type.label}-type specs only support operators: {', '.join(operator.label for operator in left_spec.type.supported_operators)}"
            )
        comparison = SpecComparison(
            left_id=id, right_id=right_spec.id, operator=operator
        )
        # new_comparisons.add(comparison)
        db.add(comparison)
    await db.commit()
