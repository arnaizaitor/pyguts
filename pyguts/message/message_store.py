from typing import (
    Dict,
    List,
)

from pyguts.gtyping import MessageLocationTuple
from pyguts.message.message import Message
from pyguts.logger.logger import logger  # noqa: E402
from pyguts.utils import singleton


@singleton
class MessageStore:
    """Store messages and maintain a 1-1 relation between msg_id and symbol."""

    def __init__(self) -> None:
        """Initialize the message store."""

        logger.info("Initializing the message store...")
        self._message_store: List[Message] = []

    def add_message(self, message: Message) -> None:
        """Add a message to the store."""

        logger.debug(f"Adding message to store: {message}")
        self._message_store.append(message)

    def get_messages(self) -> List[Message]:
        """Return all the messages stored."""
        return self._message_store

    def get_messages_sorted_by_location(self) -> List[Message]:
        """Return the messages sorted by location."""
        return sorted(self._message_store, key=lambda x: (x.abspath, x.line, x.column))

    def __len__(self) -> int:
        """Return the number of messages stored."""
        return len(self._message_store)
