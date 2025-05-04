from enum import IntEnum


class CategoryStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0

    @property
    def label(self):
        return {
            CategoryStatus.ACTIVE: "Active",
            CategoryStatus.INACTIVE: "Inactive",
        }[self]


class SpecType(IntEnum):
    STR = 1
    NUM = 2

    @property
    def label(self):
        return {
            SpecType.STR: "Text",
            SpecType.NUM: "Number",
        }[self]

    @property
    def supported_operators(self):
        return {
            SpecType.STR: {SpecComparisonOperator.EQ, SpecComparisonOperator.NE},
            SpecType.NUM: {
                SpecComparisonOperator.EQ,
                SpecComparisonOperator.NE,
                SpecComparisonOperator.GE,
                SpecComparisonOperator.LE,
            },
        }[self]


class SpecStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 0

    @property
    def label(self):
        return {
            SpecStatus.ACTIVE: "In-use",
            SpecStatus.INACTIVE: "Inactive",
        }[self]


class SpecComparisonOperator(IntEnum):
    EQ = 1
    NE = 2
    GE = 3
    LE = 4

    def compare(self, left: str, right: str):
        return {
            SpecComparisonOperator.EQ: left == right,
            SpecComparisonOperator.NE: left != right,
            SpecComparisonOperator.GE: float(left) >= float(right),
            SpecComparisonOperator.LE: float(left) <= float(right),
        }[self]

    @property
    def label(self):
        return {
            SpecComparisonOperator.EQ: "=",
            SpecComparisonOperator.NE: "<>",
            SpecComparisonOperator.GE: ">=",
            SpecComparisonOperator.LE: "<=",
        }[self]

    def flip(self):
        return {
            SpecComparisonOperator.EQ: SpecComparisonOperator.EQ,
            SpecComparisonOperator.NE: SpecComparisonOperator.NE,
            SpecComparisonOperator.GE: SpecComparisonOperator.LE,
            SpecComparisonOperator.LE: SpecComparisonOperator.GE,
        }[self]
