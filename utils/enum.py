from datetime import datetime
from enum import IntEnum, StrEnum


class Permission(IntEnum):
    READ = 0
    WRITE = 1
    DELETE = 2


class FilterOption(StrEnum):
    IN = "IN"
    NOT_IN = "NOT_IN"
    BETWEEN = "BETWEEN"
    NOT_BETWEEN = "NOT_BETWEEN"
    ILIKE = "ILIKE"
    NOT_ILIKE = "NOT_ILIKE"
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="

    @property
    def max_args(self):
        return {
            FilterOption.BETWEEN: 2,
            FilterOption.NOT_BETWEEN: 2,
            FilterOption.IN: None,
            FilterOption.NOT_IN: None,
            FilterOption.ILIKE: 1,
            FilterOption.NOT_ILIKE: 1,
            FilterOption.LT: 1,
            FilterOption.GT: 1,
            FilterOption.LTE: 1,
            FilterOption.GTE: 1,
        }[self]

    @property
    def min_args(self):
        return {
            FilterOption.BETWEEN: 2,
            FilterOption.NOT_BETWEEN: 2,
            FilterOption.IN: 1,
            FilterOption.NOT_IN: 1,
            FilterOption.ILIKE: 1,
            FilterOption.NOT_ILIKE: 1,
            FilterOption.LT: 1,
            FilterOption.GT: 1,
            FilterOption.LTE: 1,
            FilterOption.GTE: 1,
        }[self]

    def supported_types(self):
        return {
            FilterOption.IN: (
                list,
                tuple,
            ),
            FilterOption.NOT_IN: (list, tuple),
            FilterOption.ILIKE: (str,),
            FilterOption.NOT_ILIKE: (str,),
            FilterOption.BETWEEN: (list, tuple),
            FilterOption.NOT_BETWEEN: (list, tuple),
            FilterOption.LT: (int, float, str, datetime),
            FilterOption.GT: (int, float, str, datetime),
            FilterOption.LTE: (int, float, str, datetime),
            FilterOption.GTE: (int, float, str, datetime),
        }[self]
