class TaskApplicationError(Exception):
    """Base exception for the task application layer."""


class InvalidTaskDataError(TaskApplicationError):
    def __init__(self, message: str = "Task data cannot be None"):
        super().__init__(message)


class TaskNotFoundError(TaskApplicationError):
    def __init__(self, task_id: int):
        super().__init__(f"Task with id {task_id} was not found")
        self.task_id = task_id


class NoTasksFoundError(TaskApplicationError):
    def __init__(self, message: str = "No tasks were found"):
        super().__init__(message)


class TaskPersistenceError(TaskApplicationError):
    def __init__(self, operation: str, original_error: Exception):
        super().__init__(f"Failed to {operation} task: {original_error}")
        self.operation = operation
        self.original_error = original_error
