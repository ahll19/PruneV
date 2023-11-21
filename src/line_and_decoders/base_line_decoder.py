from typing import List
from abc import ABC, abstractmethod

from .line import Line


class BaseLineDecoder(ABC):
    header: List[str]
    footer: List[str]

    @abstractmethod
    def __init__(self, header: str, footer: str) -> None:
        pass

    @abstractmethod
    def decode_line(self, line: str) -> Line:
        pass
