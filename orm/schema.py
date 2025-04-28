from typing import Generic, TypeVar

from sqlalchemy import asc, desc, select
from database.models import Entity
from utils.enum import FilterOption
from utils.schema import FieldFilterCriteria, FieldPriorityCriteria, QueryRequest


T = TypeVar("T", bound=Entity)

class SQLAlchemyFieldFilterCriteria(FieldFilterCriteria):

    def to_sql_filter(self):
        column = getattr(self.entity, self.attribute)
        inner_type = column.type.python_type
        values = [inner_type(value) for value in self.values]
        operations = {
            FilterOption.BETWEEN: lambda: column.between(
                cleft=self.values[0], cright=values[1]
            ),
            FilterOption.NOT_BETWEEN: lambda: ~column.between(
                cleft=self.values[0], cright=values[1]
            ),
            FilterOption.IN: lambda: column.in_(other=values),
            FilterOption.NOT_IN: lambda: column.not_in(other=values),
            FilterOption.ILIKE: lambda: column.ilike(other=values[0]),
            FilterOption.NOT_ILIKE: lambda: column.not_ilike(other=values[0]),
            FilterOption.LT: lambda: column < values[0],
            FilterOption.GT: lambda: column > values[0],
            FilterOption.LTE: lambda: column <= values[0],
            FilterOption.GTE: lambda: column >= values[0],
        }
        return operations[self.option]()
    
class SQLAlchemyFieldPriorityCriteria(FieldPriorityCriteria):

    def to_sql_priority(self):
        priority = asc if self.asc else desc
        return priority(column=getattr(self.entity, self.attribute))
    
class SQLAlchemyQueryRequest(QueryRequest, Generic[T]):
    def to_sql_query(self):
        query = select(type(T)).filter(
            *(filter.to_sql_filter() for filter in self.resolve_filters()),
        ).order_by(
            *(priority.to_sql_priority() for priority in self.resolve_priorities()),
        )
        return query
