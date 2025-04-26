from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

from database.models.enum import SpecType


class CreateSpecRequest(BaseModel):
    category_id: Annotated[int, Field(gt=0)]
    label: Annotated[str, Field(min_length=1, max_length=50)]
    type: Annotated[SpecType, Field()]
    units: Annotated[set[str], Field(min_length=1, max_length=5)]
    filterable: Annotated[bool, Field(...)]

class CreateSpecResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    label: str
    type: SpecType
    units: set[str]
    filterable: bool
