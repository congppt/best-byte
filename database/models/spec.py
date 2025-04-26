from typing import TYPE_CHECKING
from sqlalchemy import ARRAY, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Entity
from database.models.category import Category
from database.models.enum import SpecType

if TYPE_CHECKING:
    from database.models.category import Category


class Spec(Entity):
    __tablename__ = "spec"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    label: Mapped[str]
    type: Mapped[SpecType] = mapped_column(
        Enum(SpecType, native_enum=False, validate_strings=True)
    )
    units: Mapped[list[str]] = mapped_column(ARRAY(String))
    filterable: Mapped[bool]

    category: Mapped["Category"] = relationship(back_populates="specs")
    __table_args__ = (UniqueConstraint("category_id", "label"),)
