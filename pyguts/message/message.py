from dataclasses import asdict, dataclass

from pyguts.constants import MSG_TYPES
from pyguts.interfaces import UNDEFINED, Confidence
from pyguts.gtyping import MessageLocationTuple, ExtraMessageOptions


@dataclass(unsafe_hash=True)
class Message:  # pylint: disable=too-many-instance-attributes
    """This class represent a message to be issued by the reporters."""

    msg_id: str
    symbol: str
    msg: str
    C: str
    category: str
    confidence: Confidence
    abspath: str
    path: str
    module: str
    obj: str
    line: int
    column: int
    end_line: int | None
    end_column: int | None
    options: ExtraMessageOptions | None = None

    def __init__(
        self,
        msg_id: str,
        symbol: str,
        location: MessageLocationTuple,
        msg: str,
        confidence: Confidence | None,
        options: ExtraMessageOptions | None = None,
    ) -> None:
        self.msg_id = msg_id
        self.symbol = symbol
        self.msg = msg
        self.C = msg_id[0]
        self.category = MSG_TYPES[msg_id[0]]
        self.confidence = confidence or UNDEFINED
        self.abspath = location.abspath
        self.path = location.path
        self.module = location.module
        self.obj = location.obj
        self.line = location.line
        self.column = location.column
        self.end_line = location.end_line
        self.end_column = location.end_column
        self.options = options

    def __repr__(self) -> str:
        return f"{self.format('{symbol} - {msg_id} - {msg}')}"

    def format(self, template: str) -> str:
        """Format the message according to the given template.

        The template format is the one of the format method :
        cf. https://docs.python.org/2/library/string.html#formatstrings
        """
        return template.format(**asdict(self))

    @property
    def location(self) -> MessageLocationTuple:
        return MessageLocationTuple(
            self.abspath,
            self.path,
            self.module,
            self.obj,
            self.line,
            self.column,
            self.end_line,
            self.end_column,
        )
