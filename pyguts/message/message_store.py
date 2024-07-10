from typing import Dict

from pyguts.gtyping import MessageLocationTuple

from pyguts.message.message import Message


class MessageStore:
    """Store messages and maintain a 1-1 relation between msg_id and symbol."""

    def __init__(self) -> None:
        self._message_store: List[Message] = []

    def add_message(self, message: Message) -> None:
        """Add a message to the store."""
        if (
            message.msg_id in self._message_store
            or message.symbol in self._message_store
        ):
            raise ValueError("Message ID or symbol already exists in the store.")

        self._message_store.append(message)

    def get_messages_sorted_by_location(self) -> List[Message]:
        """Return the messages sorted by location."""
        return sorted(self._message_store, key=lambda x: (x.abspath, x.line, x.column))

    def __len__(self) -> int:
        """Return the number of messages stored."""
        return len(self._message_store)
