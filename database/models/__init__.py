from sqlalchemy import MetaData, inspect
from sqlalchemy.orm import DeclarativeBase


class Entity(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_[%(column_0_N_name)s]",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_[%(column_0_name)s]_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    @classmethod
    def from_dict(cls, **dict):
        """
        Convert dict to SQLAlchemy entity, skip invalid columns.
        """
        mapper = inspect(cls)
        columns = {column.key for column in mapper.attrs}

        # Filter Pydantic dict to valid SQLAlchemy fields
        filtered_data = {k: v for k, v in dict.items() if k in columns}

        return cls(**filtered_data)
