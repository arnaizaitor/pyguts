from abc import ABC, abstractmethod
from pyguts.message.message_store import MessageStore


class BaseReporter(ABC):
    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        self._message_store: MessageStore = MessageStore()

    @abstractmethod
    def report(self):
        """Generate a report from the messages stored in the MessageStore."""
        raise NotImplementedError
