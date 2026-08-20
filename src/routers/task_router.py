from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from .task_dtos import (
    CreateTaskDTO,
    UpdateTaskDTO,
    CompleteTaskDTO,
    DeleteTaskDTO,
    TaskResponseDTO,
)
from ..application.task_application import TaskApplication
from ..application.exeptions import (
    InvalidTaskDataError,
    TaskNotFoundError,
    NoTasksFoundError,
    TaskPersistenceError,
)
from ..data_access.database.datebase_connection import get_session
from ..data_access.task_repository import TaskRepository
from ..model.services.ws_notifier import WsNotifier

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


def get_task_application(session: Session = Depends(get_session)) -> TaskApplication:
    return TaskApplication(TaskRepository(session), WsNotifier())


@router.post("/register", response_model=TaskResponseDTO, status_code=status.HTTP_201_CREATED)
def register_task(task_dto: CreateTaskDTO, task_app: TaskApplication = Depends(get_task_application)):
    try:
        return task_app.register_task(task_dto)
    except InvalidTaskDataError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(error)) from error
    except TaskPersistenceError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)) from error

@router.put("/{task_id}", response_model=TaskResponseDTO)
def update_task(task_id: int, task_dto: UpdateTaskDTO, task_app: TaskApplication = Depends(get_task_application)):
    task_dto.id = task_id
    try:
        return task_app.update_task(task_dto)
    except InvalidTaskDataError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(error)) from error
    except TaskNotFoundError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(error)) from error
    except TaskPersistenceError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)) from error

@router.get("/{task_id}", response_model=TaskResponseDTO)
def get_task_by_id(task_id: int, task_app: TaskApplication = Depends(get_task_application)):
    try:
        return task_app.get_task(task_id)
    except TaskNotFoundError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(error)) from error
    except TaskPersistenceError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)) from error

@router.get("/", response_model=List[TaskResponseDTO])
def get_all_tasks(task_app: TaskApplication = Depends(get_task_application)):
    try:
        return task_app.get_all_tasks()
    except NoTasksFoundError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(error)) from error
    except TaskPersistenceError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)) from error

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, task_app: TaskApplication = Depends(get_task_application)):
    try:
        task_app.delete_task(DeleteTaskDTO(id=task_id))
    except TaskNotFoundError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(error)) from error
    except TaskPersistenceError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)) from error

@router.put("/{task_id}/complete", response_model=TaskResponseDTO)
def complete_task(task_id: int, task_app: TaskApplication = Depends(get_task_application)):
    try:
        return task_app.complete_task(CompleteTaskDTO(id=task_id))
    except TaskNotFoundError as error:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(error)) from error
    except TaskPersistenceError as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)) from error
