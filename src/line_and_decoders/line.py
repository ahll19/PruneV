from dataclasses import dataclass
from typing import Dict

from ..register import Register


@dataclass(order=True, frozen=True)
class Line:
    cycle: int
    instruction: str
    instruction_kwargs: Dict[str, int | Register]
