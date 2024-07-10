from typing import NamedTuple
from dataclasses import dataclass

__all__ = ("HIGH",)


@dataclass
class Confidence:
    name: str
    description: str


# Warning Certainties
HIGH = Confidence("HIGH", "Warning that is not based on inference result.")
