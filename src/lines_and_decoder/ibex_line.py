from  import BaseLine

from typing import Dict


class IbexLine(BaseLine):
    time: int
    pc: int
    encoded_instruction: int
    memory_content: Dict[int, int]
