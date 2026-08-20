from typing import List

from ..data_access.Itask_repository import ITaskRepository
from ..model.services.Inotifier import Inotifier
from ..model.entities.task import Task
from ..routers.task_dtos import *
from .task_mapper import TaskMapper as task_mapper
from .exeptions import (
    InvalidTaskDataError,
    TaskNotFoundError,
    NoTasksFoundError,
    TaskPersistenceError,
)

class TaskApplication:
    def __init__(self, task_repo: ITaskRepository, notifier: Inotifier):
        self.__task_repo = task_repo
        self.__notifier = notifier

    def register_task(self, task_dto: CreateTaskDTO):
        if task_dto is None:
            raise InvalidTaskDataError()
        task = task_mapper.to_entity(task_dto)

        try:
            created_task = self.__task_repo.create_task(task)
        except Exception as error:
            raise TaskPersistenceError("create", error) from error

        self.__notifier.send_notification(created_task)

        return task_mapper.to_response_dto(created_task)


    def update_task(self, task_dto: UpdateTaskDTO):
        if task_dto is None:
            raise InvalidTaskDataError()

        try:
            task = self.__task_repo.get_by_id(task_dto.id)
        except Exception as error:
            raise TaskPersistenceError("get_by_id", error) from error

        if task is None:
            raise TaskNotFoundError(task_dto.id)

        task_updated = task_mapper.apply_update(task, task_dto)

        try:
            saved_task = self.__task_repo.update_task(task_updated)
        except Exception as error:
            raise TaskPersistenceError("update", error) from error

        return task_mapper.to_response_dto(saved_task)

    def complete_task(self, task_completed: CompleteTaskDTO):
        if task_completed is None:
            raise InvalidTaskDataError()

        try:
            task: Task = self.__task_repo.get_by_id(task_completed.id)
        except Exception as error:
            raise TaskPersistenceError("get_by_id", error) from error

        if task is None:
            raise TaskNotFoundError(task_completed.id)

        task.mark_completed()

        try:
            saved_task = self.__task_repo.update_task(task)
        except Exception as error:
            raise TaskPersistenceError("update", error) from error

        self.__notifier.send_notification(saved_task)

        return task_mapper.to_response_dto(saved_task)

    def get_task(self, task_id: int):
        try:
            task = self.__task_repo.get_by_id(task_id)
        except Exception as error:
            raise TaskPersistenceError("get_by_id", error) from error

        if task is None:
            raise TaskNotFoundError(task_id)

        return task_mapper.to_response_dto(task)

    def delete_task(self, delete_task_dto: DeleteTaskDTO):
        if delete_task_dto is None:
            raise InvalidTaskDataError()

        try:
            task = self.__task_repo.get_by_id(delete_task_dto.id)
        except Exception as error:
            raise TaskPersistenceError("get_by_id", error) from error

        if task is None:
            raise TaskNotFoundError(delete_task_dto.id)

        try:
            self.__task_repo.delete_task(delete_task_dto.id)
        except Exception as error:
            raise TaskPersistenceError("delete", error) from error

    def get_all_tasks(self):
        try:
            tasks: List[Task] = self.__task_repo.get_all()
        except Exception as error:
            raise TaskPersistenceError("get_all", error) from error

        if not tasks:
            raise NoTasksFoundError()

        tasks_dto: List[TaskResponseDTO] = []
        for task in tasks:
            tasks_dto.append(task_mapper.to_response_dto(task))
        return tasks_dto