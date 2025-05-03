from __future__ import annotations
from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, reconstructor

from database.models import Entity
from database.models.enum import (
    CategoryStatus,
    SpecComparisonOperator,
    SpecStatus,
    SpecType,
)


class Category(Entity):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("category.id"))
    icon: Mapped[str | None]
    status: Mapped[CategoryStatus] = mapped_column(
        Enum(CategoryStatus, native_enum=False, validate_strings=True)
    )

    parent: Mapped[Category] = relationship(
        back_populates="children", foreign_keys=[parent_id]
    )
    children: Mapped[set[Category]] = relationship(
        back_populates="parent", remote_side=id
    )
    specs: Mapped[list[Spec]] = relationship(
        back_populates="category",
    )

    __table_args__ = (CheckConstraint("parent_id != id", name="self_reference"),)


class SpecComparison(Entity):
    __tablename__ = "spec_comparison"
    left_id: Mapped[int] = mapped_column(ForeignKey("spec.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(ForeignKey("spec.id"), primary_key=True)
    operator: Mapped[SpecComparisonOperator] = mapped_column(
        Enum(SpecComparisonOperator, native_enum=False, validate_strings=True)
    )
    left: Mapped[Spec] = relationship(foreign_keys=[left_id])
    right: Mapped[Spec] = relationship(foreign_keys=[right_id])

    __table_args__ = (CheckConstraint("left_id != right_id", name="self_comparison"),)


class Spec(Entity):
    __tablename__ = "spec"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    label: Mapped[str]
    type: Mapped[SpecType] = mapped_column(
        Enum(SpecType, native_enum=False, validate_strings=True)
    )
    units: Mapped[set[str]] = mapped_column(ARRAY(String))
    filterable: Mapped[bool]
    status: Mapped[SpecStatus] = mapped_column(
        Enum(SpecStatus, native_enum=False, validate_strings=True)
    )

    category: Mapped[Category] = relationship(back_populates="specs")
    left_comparisons: Mapped[set[SpecComparison]] = relationship(
        back_populates="right", foreign_keys=[SpecComparison.right_id]
    )
    right_comparisons: Mapped[set[SpecComparison]] = relationship(
        back_populates="left", foreign_keys=[SpecComparison.left_id]
    )

    __table_args__ = (UniqueConstraint("category_id", "label"),)

    @reconstructor
    def init_on_load(self):
        self.units = set(self.units)
