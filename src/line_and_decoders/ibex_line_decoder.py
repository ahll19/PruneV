from typing import Dict

from ..instructions.instruction_factory import InstructionLibrary, InstructionFactory
from ..register import Register
from .base_line_decoder import BaseLineDecoder
from .line import Line


class IbexLineDecoder(BaseLineDecoder):
    def __init__(self, header: str, footer: str) -> None:
        self.header = [x.strip() for x in header.split("\t")]
        self.footer = [x.strip() for x in footer.split("\t")]

    def decode_line(self, line: str) -> Line:
        split_line = line.split("\t")
        split_line = [x.strip() for x in split_line]
        last_element = split_line.pop(-1).strip()
        split_line[-1] += " " + last_element

        instruction = InstructionFactory.get_instruction(
            InstructionLibrary.RISCV, split_line[4]
        )

        instruction_kwargs = self._get_kwargs_for_instruction(
            instruction.format, split_line[5]
        )

        line = Line(
            cycle=int(split_line[1]),
            instruction=split_line[4],
            instruction_kwargs=instruction_kwargs,
        )

        return line

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
                    imm = int(imm) if "0x" not in imm else int(imm, 16)
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
                    imm = int(imm) if "0x" not in imm else int(imm, 16)
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
            case "Undefined":
                _r = memory_content.split(" ")[0]
                regs = [
                    Register(int(r[1:])) for r in _r.split(",") if r.startswith("x")
                ]
                kwargs = {
                    "regs": regs,
                }
            case _:
                raise NotImplementedError(
                    f"Instruction format {instruction_format} not implemented"
                )

        return kwargs
