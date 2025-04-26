from typing import TYPE_CHECKING
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Entity
from database.models.enum import CategoryStatus

if TYPE_CHECKING:
    from database.models.spec import Spec


class Category(Entity):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("category.id"))
    icon: Mapped[str | None]
    status: Mapped[CategoryStatus] = mapped_column(
        Enum(CategoryStatus, native_enum=False, validate_strings=True)
    )

    parent: Mapped["Category"] = relationship(back_populates="children", remote_side=parent_id)
    children: Mapped[set["Category"]] = relationship(back_populates="parent", remote_side=id)
    specs: Mapped[list["Spec"]] = relationship(
        "Spec",
        back_populates="category",
    )
