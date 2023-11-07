from instruction_factory import InstructionFactory
from base_instructions import Instruction
from register import Register

from typing import Dict, Tuple


class InstructionFormatter:
    @classmethod
    def format(
        cls, instruction: str, memory_content: str
    ) -> Tuple[Instruction, Dict[str, Register | int]] | None:
        instruction = InstructionFactory.get_instruction(instruction)
        if instruction is None:
            return None, None

        instruction_format = instruction.format
        kwargs_for_instruction = cls._get_kwargs_for_instruction(
            instruction_format, memory_content
        )

        return instruction, kwargs_for_instruction

    @classmethod
    def _get_kwargs_for_instruction(
        cls, instruction_format: str, memory_content: str
    ) -> Dict[str, Register | int] | None:
        match instruction_format:
            case "UJ":
                rd, imm = memory_content.split(" ")[0].split(",")
                rd = Register(int(rd[1:]))
                imm = int(imm, 16)
                kwargs = {
                    "rd": rd,
                    "imm": imm,
                }
            case "I":
                insane_formatting = "(" in memory_content and ")" in memory_content
                if not insane_formatting:
                    rd, rs1, imm = memory_content.split(" ")[0].split(",")
                    rd = Register(int(rd[1:]))
                    rs1 = Register(int(rs1[1:]))
                    imm = int(imm) if not "0x" in imm else int(imm, 16)
                    kwargs = {
                        "rd": rd,
                        "rs1": rs1,
                        "imm": imm,
                    }
                else:
                    first = memory_content.split(" ")[0]
                    rd, second = first.split(",")
                    rd = Register(int(rd[1:]))
                    imm, rs1 = second.split("(")
                    imm = int(imm) if not "0x" in imm else int(imm, 16)
                    rs1 = Register(int(rs1[1:-1]))
                    kwargs = {
                        "rd": rd,
                        "rs1": rs1,
                        "imm": imm,
                    }
            case "B":
                rs1, rs2, imm = memory_content.split(" ")[0].split(",")
                rs1 = Register(int(rs1[1:]))
                rs2 = Register(int(rs2[1:]))
                imm = int(imm, 16)
                kwargs = {
                    "rs1": rs1,
                    "rs2": rs2,
                    "imm": imm,
                }

            case "S":
                first = memory_content.split(" ")[0]
                rs1, second = first.split(",")
                rs1 = Register(int(rs1[1:]))
                imm, rs2 = second.split("(")
                imm = int(imm)
                rs2 = Register(int(rs2[1:-1]))
                kwargs = {
                    "rs1": rs1,
                    "rs2": rs2,
                    "imm": imm,
                }
            case "R":
                rd, rs1, rs2 = memory_content.split(" ")[0].split(",")
                rd = Register(int(rd[1:]))
                rs1 = Register(int(rs1[1:]))
                rs2 = Register(int(rs2[1:]))
                kwargs = {
                    "rd": rd,
                    "rs1": rs1,
                    "rs2": rs2,
                }
            case _:
                raise ValueError(f"Instruction format {instruction_format} not found")

        return kwargs
