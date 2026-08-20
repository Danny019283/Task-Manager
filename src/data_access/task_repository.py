from typing import List, Optional

from sqlmodel import Session, select

from .database.datebase_connection import engine
from .Itask_repository import ITaskRepository
from .task_model import TaskModel
from ..model.entities.task import Task

#supabase implementation

class TaskRepository(ITaskRepository):
    def __init__(self, session: Optional[Session] = None):
        self.__session = session

    def __get_session(self) -> Session:
        return self.__session if self.__session is not None else Session(engine)

    @staticmethod
    def __to_entity(row: TaskModel) -> Task:
        return Task(
            description=row.description,
            limit_date=row.date_limit,
            is_completed=row.is_completed,
            id=row.id,
        )

    def create_task(self, task: Task) -> Task:
        row = TaskModel(
            description=task.description,
            date_limit=task.limit_date,
            is_completed=task.is_completed,
        )
        session = self.__get_session()
        try:
            session.add(row)
            session.commit()
            session.refresh(row)
            return self.__to_entity(row)
        finally:
            if self.__session is None:
                session.close()

    def update_task(self, task: Task) -> Task:
        session = self.__get_session()
        try:
            row = session.get(TaskModel, task.id)
            row.description = task.description
            row.date_limit = task.limit_date
            row.is_completed = task.is_completed
            session.add(row)
            session.commit()
            session.refresh(row)
            return self.__to_entity(row)
        finally:
            if self.__session is None:
                session.close()

    def get_by_id(self, id_task: int) -> Optional[Task]:
        session = self.__get_session()
        try:
            row = session.get(TaskModel, id_task)
            return self.__to_entity(row) if row is not None else None
        finally:
            if self.__session is None:
                session.close()

    def get_all(self) -> List[Task]:
        session = self.__get_session()
        try:
            rows = session.exec(select(TaskModel)).all()
            return [self.__to_entity(row) for row in rows]
        finally:
            if self.__session is None:
                session.close()

    def delete_task(self, id: int) -> None:
        session = self.__get_session()
        try:
            row = session.get(TaskModel, id)
            if row is not None:
                session.delete(row)
                session.commit()
        finally:
            if self.__session is None:
                session.close()
