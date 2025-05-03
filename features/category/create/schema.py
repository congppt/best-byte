from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict

from database.models.enum import CategoryStatus


class CreateCategoryRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Annotated[str, Field(min_length=1, max_length=50)]
    parent_id: Annotated[int | None, Field(ge=0)]
    icon: Annotated[str | None, Field(pattern=r"^<svg.*?>.*?</svg>$")]
    status: Annotated[CategoryStatus, Field(default=CategoryStatus.ACTIVE)]


class CreateCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # name: str
    # parent_id: int | None
    # icon: str | None
    # status: CategoryStatus
