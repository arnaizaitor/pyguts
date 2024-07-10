from pyguts.exceptions import (
    UnknownMessageError,
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

        self.check_msgid_and_symbol(msgid, symbol)
        self.__msgid_to_symbol[msgid] = symbol
        self.__symbol_to_msgid[symbol] = msgid

    def check_msgid_and_symbol(self, msgid: str, symbol: str) -> None:
        existing_msgid: str | None = self.__symbol_to_msgid.get(symbol)
        existing_symbol: str | None = self.__msgid_to_symbol.get(msgid)
        if existing_symbol is None and existing_msgid is None:
            return  # both symbol and msgid are usable
        if existing_msgid is not None:
            if existing_msgid != msgid:
                self._raise_duplicate_msgid(symbol, msgid, existing_msgid)
        if existing_symbol and existing_symbol != symbol:
            # See https://github.com/python/mypy/issues/10559
            self._raise_duplicate_symbol(msgid, symbol, existing_symbol)

    @staticmethod
    def _raise_duplicate_symbol(msgid: str, symbol: str, other_symbol: str) -> NoReturn:
        """Raise an error when a symbol is duplicated."""
        symbols = [symbol, other_symbol]
        symbols.sort()
        error_message = f"Message id '{msgid}' cannot have both "
        error_message += f"'{symbols[0]}' and '{symbols[1]}' as symbolic name."
        raise InvalidMessageError(error_message)

    @staticmethod
    def _raise_duplicate_msgid(symbol: str, msgid: str, other_msgid: str) -> NoReturn:
        """Raise an error when a msgid is duplicated."""
        msgids = [msgid, other_msgid]
        msgids.sort()
        error_message = (
            f"Message symbol '{symbol}' cannot be used for "
            f"'{msgids[0]}' and '{msgids[1]}' at the same time."
            f" If you're creating an 'old_names' use 'old-{symbol}' as the old symbol."
        )
        raise InvalidMessageError(error_message)
