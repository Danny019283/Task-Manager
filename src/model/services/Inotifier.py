from abc import ABC, abstractmethod
from ..entities.task import Task

class Inotifier(ABC):
    @abstractmethod
    def send_notification(self, task: Task) -> None:
        pass