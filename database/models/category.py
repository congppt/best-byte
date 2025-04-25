from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Entity
from database.models.enum import CategoryStatus


class Category(Entity):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("category.id"))
    icon: Mapped[str | None]
    status: Mapped[CategoryStatus] = mapped_column(Enum(CategoryStatus, native_enum=False, validate_strings=True))