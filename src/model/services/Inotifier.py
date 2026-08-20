from abc import ABC, abstractmethod
from ..entities.task import Task

class Inotifier(ABC):
    @abstractmethod
    def send_notification(self, from_user: str, to_user: str, task: Task):
        pass