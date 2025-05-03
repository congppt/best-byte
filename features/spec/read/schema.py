from typing import Annotated
from pydantic import BaseModel, Field

from database.models.enum import SpecType
from utils.schema import PageRequest

class SpecRequest(PageRequest):
    category_id: Annotated[int, Field(gt=0)]
    label: Annotated[str | None, Field(default=None)]

class SpecResponse(BaseModel):
    id: int
    category_id: int
    label: str
    type: SpecType
    units: set[str]
    filterable: bool
    has_comparisons: bool