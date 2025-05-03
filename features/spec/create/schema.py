from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, model_validator

from database.models.enum import SpecComparisonOperator, SpecStatus, SpecType


class CreateSpecRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    category_id: Annotated[int, Field(gt=0)]
    label: Annotated[str, Field(min_length=1, max_length=50)]
    type: Annotated[SpecType, Field(default=SpecType.STR)]
    units: Annotated[set[str], Field(default={}, max_length=5)]
    filterable: Annotated[bool, Field(default=False)]
    status: Annotated[SpecStatus, Field(default=SpecStatus.ACTIVE)]
    comparisons: Annotated[dict[int, SpecComparisonOperator], Field(default={})]

    @model_validator(mode="after")
    def validate(self):
        if self.type == SpecType.STR and self.units:
            raise ValueError("Units are not allowed for string type")
        for id in self.comparisons.keys():
            if id <= 0:
                raise ValueError(f"Compared spec id {id} is not existed")
            if self.type == SpecType.STR and self.comparisons[id] not in {
                SpecComparisonOperator.EQ,
                SpecComparisonOperator.NE,
            }:
                raise ValueError("String type only allow equals/not equals comparison")
        return self


class CreateSpecResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # category_id: int
    # label: str
    # type: SpecType
    # units: set[str]
    # filterable: bool
