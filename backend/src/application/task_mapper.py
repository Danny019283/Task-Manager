from ..model.entities.task import Task
from ..routers.task_dtos import CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO


class TaskMapper:
    @staticmethod
    def to_entity(dto: CreateTaskDTO) -> Task:
        return Task.crear(dto.description, dto.date_limit)

    @staticmethod
    def apply_update(task: Task, dto: UpdateTaskDTO) -> Task:
        return Task.actualizar(task, dto.description, dto.date_limit, dto.is_completed)

    @staticmethod
    def to_response_dto(task: Task) -> TaskResponseDTO:
        return TaskResponseDTO(
            id=task.id,
            description=task.description,
            date_limit=task.limit_date,
            is_completed=task.is_completed,
        )
