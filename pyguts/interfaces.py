from dataclasses import dataclass

__all__ = ("HIGH",)


@dataclass
class Confidence:
    name: str
    description: str


# Warning Certainties
UNDEFINED = Confidence("UNDEFINED", "Undefined certainty.")
HIGH = Confidence("HIGH", "Warning that is not based on inference result.")
