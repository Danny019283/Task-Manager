from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskModel(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    date_limit: datetime
    is_completed: bool = Field(default=False)
