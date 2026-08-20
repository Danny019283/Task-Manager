from abc import ABC, abstractmethod
from typing import List, Optional

from ..model.entities.task import Task

class ITaskRepository(ABC):
    @abstractmethod
    def create_task(self, task: Task) -> Task:
        pass

    @abstractmethod
    def update_task(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_by_id(self, id_task: int) -> Optional[Task]:
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def delete_task(self, id: int) -> None:
        pass
