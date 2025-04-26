from enum import IntEnum,StrEnum


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