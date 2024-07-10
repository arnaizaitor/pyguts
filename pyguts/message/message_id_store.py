from pyguts.exceptions import (
    DeletedMessageError,
    InvalidMessageError,
)

class MessageIdStore:
    """The MessageIdStore store MessageId and make sure that there is a 1-1 relation
    between msgid and symbol.
    """

    def __init__(self) -> None:
        self.__msgid_to_symbol: dict[str, str] = {}
        self.__symbol_to_msgid: dict[str, str] = {}
        self.__active_msgids: dict[str, list[str]] = {}

    def __len__(self) -> int:
        return len(self.__msgid_to_symbol)

    def __repr__(self) -> str:
        result = "MessageIdStore: [\n"
        for msgid, symbol in self.__msgid_to_symbol.items():
            result += f"  - {msgid} ({symbol})\n"
        result += "]"
        return result

    def get_symbol(self, msgid: str) -> str:
        try:
            return self.__msgid_to_symbol[msgid.upper()]
        except KeyError as e:
            msg = f"'{msgid}' is not a message ID stored in the message store."
            raise UnknownMessageError(msg) from e

    def get_msgid(self, symbol: str) -> str:
        try:
            return self.__symbol_to_msgid[symbol]
        except KeyError as e:
            msg = f"'{symbol}' is not a symbol stored in the message store."
            raise UnknownMessageError(msg) from e

    def add_msgid_and_symbol(self, msgid: str, symbol: str) -> None:
        """Add valid message id.

        There is a little duplication with add_legacy_msgid_and_symbol to avoid a function call,
        this is called a lot at initialization.
        """
        self.__msgid_to_symbol[msgid] = symbol
        self.__symbol_to_msgid[symbol] = msgid