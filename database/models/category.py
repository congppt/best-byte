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
    SpecComparisionOperator,
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


class SpecComparision(Entity):
    __tablename__ = "spec_comparision"
    left_id: Mapped[int] = mapped_column(ForeignKey("spec.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(ForeignKey("spec.id"), primary_key=True)
    operator: Mapped[SpecComparisionOperator] = mapped_column(
        Enum(SpecComparisionOperator, native_enum=False, validate_strings=True)
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
    # left_comparisions: Mapped[set[SpecComparision]] = relationship(
    #     back_populates="right", foreign_keys=[SpecComparision.left_id]
    # )
    # right_comparisions: Mapped[set[SpecComparision]] = relationship(
    #     back_populates="left", foreign_keys=[SpecComparision.right_id]
    # )

    __table_args__ = (UniqueConstraint("category_id", "label"),)

    @reconstructor
    def init_on_load(self):
        self.units = set(self.units)
