from datetime import datetime

class Task:
    def __init__(self, description: str, limit_date: datetime, is_completed: bool = False, id: int | None = None):
        self.validate_date(limit_date)
        self.__id = id
        self.__description = description
        self.__limit_date = limit_date
        self.__is_completed = is_completed

    @staticmethod
    def validate_date(date: datetime) -> None:
        if date < datetime.now():
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
        return not self.__is_completed and self.__limit_date < datetime.now()

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
