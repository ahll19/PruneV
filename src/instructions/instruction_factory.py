from . import riscv_instructions

from .base_instructions import Instruction

from enum import Enum


class InstructionLibrary(Enum):
    RISCV = riscv_instructions


class InstructionFactory:
    @classmethod
    def get_instruction(
        cls, instruction_library: InstructionLibrary, instruction: str
    ) -> Instruction:
        match instruction_library:
            case InstructionLibrary.RISCV:
                return cls._get_instruction_from_riscv(instruction)
            case _:
                err = f"Instruction library {instruction_library} not found in "
                err += "InstructionFactory. Please add it to the factory, or make sure"
                err += "it exists."
                raise NotImplementedError(err)

    @classmethod
    def _get_instruction_from_riscv(cls, instruction: str) -> Instruction:
        try:
            instr = instruction.upper()
            return getattr(riscv_instructions, instr)
        except AttributeError:
            raise AttributeError(f"Instruction {instr} not found in RISCV instructions")
