from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, model_validator

from database.models.enum import (
    CategoryStatus,
    SpecComparisionOperator,
    SpecStatus,
    SpecType,
)


class CreateCategoryRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Annotated[str, Field(min_length=1, max_length=50)]
    parent_id: Annotated[int | None, Field(ge=0)]
    icon: Annotated[str | None, Field(pattern=r"^<svg.*?>.*?</svg>$")]
    status: Annotated[CategoryStatus, Field(default=CategoryStatus.ACTIVE)]


class CreateSpecRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    label: Annotated[str, Field(min_length=1, max_length=50)]
    type: Annotated[SpecType, Field(default=SpecType.STR)]
    units: Annotated[set[str], Field(default={}, max_length=5)]
    filterable: Annotated[bool, Field(default=False)]
    status: Annotated[SpecStatus, Field(default=SpecStatus.ACTIVE)]
    comparisions: Annotated[dict[int, SpecComparisionOperator], Field(default={})]

    @model_validator(mode="after")
    def validate(self):
        if self.type == SpecType.STR and self.units:
            raise ValueError("Units are not allowed for string type")
        for id in self.comparisions.keys():
            if id <= 0:
                raise ValueError(f"Compared spec id {id} is not existed")
            if self.type == SpecType.STR and self.comparisions[id] not in { SpecComparisionOperator.EQ, SpecComparisionOperator.NE }:
                raise ValueError("String type only allow equals/not equals comparison")
        return self
