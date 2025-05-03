from enum import IntEnum


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


class SpecComparisonOperator(IntEnum):
    EQ = 1
    NE = 2
    GE = 3
    LE = 4

    def compare(self, left: str, right: str):
        left_val = float(left)
        right_val = float(right)
        return {
            SpecComparisonOperator.EQ: left_val == right_val,
            SpecComparisonOperator.NE: left_val != right_val,
            SpecComparisonOperator.GE: left_val >= right_val,
            SpecComparisonOperator.LE: left_val <= right_val,
        }[self]
