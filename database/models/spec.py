from sqlalchemy import ARRAY, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Entity
from database.models.enum import SpecType

class Spec(Entity):
    __tablename__ = "spec"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    label: Mapped[str]
    type: Mapped[SpecType] = mapped_column(Enum(SpecType, native_enum=False, validate_strings=True))
    units: Mapped[list[str]] = mapped_column(ARRAY(String))
    filterable: Mapped[bool]
    __table_args__ = (
        UniqueConstraint('category_id', 'label'),
    )