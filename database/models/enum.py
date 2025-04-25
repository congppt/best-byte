from enum import StrEnum


class CategoryStatus(StrEnum):
    ACTIVE = "Đang kinh doanh"
    INACTIVE = "Ngừng kinh doanh"

class SpecType(StrEnum):
    NUM = "Số"
    STR = "Văn bản"