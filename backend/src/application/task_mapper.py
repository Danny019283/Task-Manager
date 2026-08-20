from ..model.entities.task import Task
from ..routers.task_dtos import CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO


class TaskMapper:
    @staticmethod
    def to_entity(dto: CreateTaskDTO) -> Task:
        return Task(
            description=dto.description,
            limit_date=dto.date_limit,
            is_completed=dto.is_completed,
        )

    @staticmethod
    def apply_update(task: Task, dto: UpdateTaskDTO) -> Task:
        return Task(
            description=dto.description if dto.description is not None else task.description,
            limit_date=dto.date_limit if dto.date_limit is not None else task.limit_date,
            is_completed=dto.is_completed if dto.is_completed is not None else task.is_completed,
            id=task.id,
        )

    @staticmethod
    def to_response_dto(task: Task) -> TaskResponseDTO:
        return TaskResponseDTO(
            id=task.id,
            description=task.description,
            date_limit=task.limit_date,
            is_completed=task.is_completed,
        )
