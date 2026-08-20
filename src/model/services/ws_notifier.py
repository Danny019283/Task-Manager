import logging
import urllib.request
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv
import os

from .Inotifier import Inotifier
from ..entities.task import Task

load_dotenv(Path(__file__).resolve().parent / ".env")

logger = logging.getLogger(__name__)

CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


class WsNotifier(Inotifier):
    def send_notification(self, task: Task) -> None:
        phone = os.environ["CALLMEBOT_PHONE"]
        apikey = os.environ["CALLMEBOT_APIKEY"]
        text = self.__build_message(task)

        url = f"{CALLMEBOT_URL}?phone={quote(phone)}&text={quote(text)}&apikey={quote(apikey)}"

        try:
            with urllib.request.urlopen(url, timeout=10):
                pass
        except Exception as error:
            logger.warning("Failed to send WhatsApp notification via CallMeBot: %s", error)

    @staticmethod
    def __build_message(task: Task) -> str:
        status = "completada" if task.is_completed else "pendiente"
        return (
            f"Tarea: {task.description}\n"
            f"Fecha limite: {task.limit_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"Estado: {status}"
        )
