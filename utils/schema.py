from abc import ABC
import ast
from datetime import datetime
import re
from typing import Any, Generic, Sequence, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

from utils.enum import FilterOption

T = TypeVar("T")
SORTABLE_TYPES = (str, int, float, datetime)
VALUE_REGEX = re.compile(
    pattern=r"^(?:\'[^\']*\'|\d+(?:\.\d+)?|\((?:\'[^\']*\'|\d+(?:\.\d+)?(?:\s*,\s*(?:\'[^\']*\'|\d+(?:\.\d+)?))*)\))$"
)


class PageRequest(BaseModel):
    size: int = Field(default=10, gt=0, le=100)
    index: int = Field(default=0, ge=0)


class FieldBaseCriteria(BaseModel):
    entity: type
    attribute: str = Field(default=...)


class FieldFilterCriteria(ABC, FieldBaseCriteria):
    values: tuple = Field(min_length=1)
    option: FilterOption

    def to_sql_filter(self) -> Any:
        pass


class FilterRequest(BaseModel, Generic[T]):
    filters: str | None = Field(default=None)

    @field_validator("filters")
    def validate_filters(cls, v: str | None) -> str | None:
        if not v:  # Early return for None/empty
            return v
        candidates = v.split(sep=";")
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=3)
            if len(metadata) != 3:
                raise ValueError(
                    f"Invalid filter format. Expected '[attribute] [option] [values]', got: '{candidate}'"
                )
            attribute, option_str, value_str = metadata
            # Validate attribute
            if not attribute:
                raise ValueError("Attribute required")
            entity_type = cls.__pydantic_generic_metadata__["args"][0]
            if not hasattr(entity_type, attribute):
                raise ValueError(
                    f"'{attribute}' is not an attribute of {entity_type.__name__}"
                )
            # Validate option
            if option_str not in {opt.value for opt in FilterOption}:
                raise ValueError(
                    f"Invalid option '{option_str}'. Must be one of: {', '.join(opt.value for opt in FilterOption)}"
                )
            # Validate value format and type
            if not VALUE_REGEX.match(string=value_str):
                raise ValueError(
                    "Expected a string, number, or tuple of strings/numbers"
                )
            # Parse and validate values
            value = ast.literal_eval(node_or_string=value_str)
            values = tuple(value) if isinstance(value, (tuple, list, set)) else (value,)
            option = FilterOption(value=option_str)
            if option.max_args and len(values) > option.max_args:
                raise ValueError(f"Maximum {option.max_args} values allowed")
            if len(values) < option.min_args:
                raise ValueError(f"Minimum {option.min_args} values required")
            if not all(isinstance(x, type(values[0])) for x in values):
                raise ValueError("All values must be of same type")
        return v

    def resolve_filters(self):
        """Resolves filter string into FilterCriteria objects.

        Returns:
            list[FilterCriteria]: List of parsed filter criteria
        """
        if not self.filters:
            return []
        filters: list[FieldFilterCriteria] = []
        candidates = self.filters.split(sep=";")
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=3)
            value = ast.literal_eval(node_or_string=metadata[-1])
            if isinstance(value, tuple | list | set):
                values = tuple(value)
            else:
                values = (value,)
            filters.append(
                FieldFilterCriteria(
                    entity=self.__class__.__pydantic_generic_metadata__["args"][0],
                    attribute=metadata[0],
                    values=values,
                    option=FilterOption(value=metadata[-2]),
                )
            )
        return filters


class FieldPriorityCriteria(ABC, FieldBaseCriteria):
    asc: bool = Field(default=True)

    def to_sql_priority(self) -> Any:
        pass


class PriorityRequest(BaseModel, Generic[T]):
    priorities: str | None = Field(default=None)

    @field_validator("priorities")
    def validate_priorities(cls, v):
        if not v:
            return v
        candidates = v.split(sep=";")
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=1)
            if len(metadata) > 2:
                raise ValueError(
                    "Invalid priority format. Expected '[attribute] [ASC|DESC]'"
                )
            if not metadata[0]:
                raise ValueError("Attribute is required")
            entity_type = cls.__pydantic_generic_metadata__["args"][0]
            if not hasattr(entity_type, metadata[0]):
                raise ValueError(
                    f"'{metadata[0]}' is not an attribute of {entity_type.__name__}"
                )
            if len(metadata) != 1 and metadata[1] not in {"ASC", "DESC"}:
                raise ValueError("Sorting order must be ASC or DESC")
        return v

    def resolve_priorities(self):
        """Resolves priority string into PriorityCriteria objects.

        Returns:
            list[PriorityCriteria]: List of parsed priority criteria
        """
        if not self.priorities:
            return []
        priorities: list[FieldPriorityCriteria] = []
        candidates = self.priorities.split(sep=";")
        for candidate in candidates:
            metadata = candidate.split(sep=" ", maxsplit=1)
            priorities.append(
                FieldPriorityCriteria(
                    entity=self.__class__.__pydantic_generic_metadata__["args"][0],
                    attribute=metadata[0],
                    asc=len(metadata) == 1 or metadata[1] == "ASC",
                )
            )
        return priorities


class QueryRequest(ABC, PageRequest, FilterRequest[T], PriorityRequest[T], Generic[T]):
    model_config = ConfigDict(str_strip_whitespace=True)

    def to_sql_query(self):
        pass


class PageResponse(BaseModel, Generic[T]):
    items: Sequence[T]
    total_pages: int
    total_items: int
