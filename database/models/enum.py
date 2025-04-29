from enum import IntEnum
from typing import Any


class CategoryStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0

    @property
    def label(self):
        return {
            CategoryStatus.ACTIVE: "Đang kinh doanh",
            CategoryStatus.INACTIVE: "Ngừng kinh doanh",
        }[self]


class SpecType(IntEnum):
    STR = 1
    NUM = 2

    @property
    def label(self):
        return {
            SpecType.STR: "Văn bản",
            SpecType.NUM: "Số",
        }[self]


class SpecStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0

    @property
    def label(self):
        return {
            SpecStatus.ACTIVE: "Đang sử dụng",
            SpecStatus.INACTIVE: "Ngừng sử dụng",
        }[self]


class SpecComparisionOperator(IntEnum):
    EQ = 1
    NE = 2
    GE = 3
    LE = 4

    def compare(self, left: str, right: str):
        left_val = float(left)
        right_val = float(right)
        return {
            SpecComparisionOperator.EQ: left_val == right_val,
            SpecComparisionOperator.NE: left_val != right_val,
            SpecComparisionOperator.GE: left_val >= right_val,
            SpecComparisionOperator.LE: left_val <= right_val,
        }[self]
