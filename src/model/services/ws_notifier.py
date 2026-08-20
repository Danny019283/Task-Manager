from .Inotifier import Inotifier
from ..entities.task import Task

class WsNotifier(Inotifier):
    def send_notification(self, from_user: str, to_user: str, task: Task):
            pass #notify by whatsapp through CallMeBot