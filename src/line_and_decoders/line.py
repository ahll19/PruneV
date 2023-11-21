from dataclasses import dataclass
from typing import Any, Dict

from ..register import Register
from ..instructions.base_instructions import Instruction


@dataclass(order=True, frozen=True)
class Line:
    cycle: int
    instruction: str
    instruction_kwargs: Dict[str, int | Register]
