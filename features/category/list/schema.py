from typing import Annotated
from pydantic import BaseModel, Field
from database.models.enum import CategoryStatus
from utils.schema import PageRequest

class CategoryRequest(PageRequest):
    name: Annotated[str | None, Field(default=None)]
    status: Annotated[CategoryStatus | None, Field(default=None)]

class BaseCategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: int | None
    icon: str | None
    status: CategoryStatus
    has_children: bool
