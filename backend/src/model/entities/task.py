from datetime import datetime
from zoneinfo import ZoneInfo

_COSTA_RICA_TZ = ZoneInfo("America/Costa_Rica")


def _now() -> datetime:
    return datetime.now(_COSTA_RICA_TZ).replace(tzinfo=None)


class Task:
    def __init__(self, description: str, limit_date: datetime, is_completed: bool = False, id = None):
        self.__id = id
        self.__description = description
        self.__limit_date = limit_date
        self.__is_completed = is_completed
        
    @classmethod
    def crear(cls, description: str, limit_date: datetime):
        cls._validate_date(limit_date)
        return cls(description, limit_date, False, None)

    @classmethod
    def actualizar(cls, task: "Task", description: str = None, limit_date: datetime = None, is_completed: bool = None) -> "Task":
        if limit_date is not None:
            cls._validate_date(limit_date)
        return cls(
            description=description if description is not None else task.description,
            limit_date=limit_date if limit_date is not None else task.limit_date,
            is_completed=is_completed if is_completed is not None else task.is_completed,
            id=task.id,
        )

    @staticmethod
    def _validate_date(date: datetime) -> None:
        if date < _now():
            raise ValueError("limit_date cannot be earlier than the current date")

    @property
    def id(self) -> int | None:
        return self.__id

    @property
    def description(self) -> str:
        return self.__description

    @property
    def limit_date(self) -> datetime:
        return self.__limit_date

    @property
    def is_completed(self) -> bool:
        return self.__is_completed

    def mark_completed(self) -> None:
        self.__is_completed = True

    def is_overdue(self) -> bool:
        return not self.__is_completed and self.__limit_date < _now()

    def __repr__(self) -> str:
        return (
            f"Task(description={self.__description!r}, "
            f"limit_date={self.__limit_date!r}, is_completed={self.__is_completed!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.__description == other.__description
            and self.__limit_date == other.__limit_date
            and self.__is_completed == other.__is_completed
        )
