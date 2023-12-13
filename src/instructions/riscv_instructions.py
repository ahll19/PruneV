from ..register import Register
from .base_instructions import (
    InstructionB,
    InstructionI,
    InstructionS,
    InstructionUJ,
    InstructionR,
)

from typing import List


"""
Some of these instructions say they dont override, but if LUI and AUIPC are called on
the same register in immediate succesion they will override. Looking at combinations of
different instructions might be a good idea of this proof of concept works.
"""


class LUI(InstructionUJ):
    @staticmethod
    def overrides(rd: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, imm: int) -> List[Register]:
        return []


class AUIPC(InstructionUJ):
    @staticmethod
    def overrides(rd: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, imm: int) -> List[Register]:
        return []


class JAL(InstructionUJ):
    @staticmethod
    def overrides(rd: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, imm: int) -> List[Register]:
        return []


class JALR(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class BEQ(InstructionB):
    @staticmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return []

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return [rs1, rs2]


class BNE(InstructionB):
    @staticmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return []

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return [rs1, rs2]


class BLT(InstructionB):
    @staticmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return []

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return [rs1, rs2]


class BGE(InstructionB):
    @staticmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return []

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return [rs1, rs2]


class BLTU(InstructionB):
    @staticmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return []

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return [rs1, rs2]


class BGEU(InstructionB):
    @staticmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return []

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return [rs1, rs2]


class LB(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class LH(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class LW(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        if rd != rs1:
            return [rd]
        else:
            return []

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class LBU(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class LHU(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class SB(InstructionS):
    @staticmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return []

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return [rs1, rs2]


class SH(InstructionS):
    @staticmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return []

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return [rs1, rs2]


class SW(InstructionS):
    @staticmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return []

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register]:
        return [rs1, rs2]


class ADDI(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        if rd != rs1:
            return [rd]
        else:
            return []

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class SLTI(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class SLTIU(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class XORI(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class ORI(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class ANDI(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class SLLI(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        if rd == rs1:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class SRLI(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        if rd == rs1:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class SRAI(InstructionI):
    @staticmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register]:
        if rd == rs1:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register]:
        return [rs1]


class ADD(InstructionR):
    @staticmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        if rd == rs1 or rd == rs2:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        return [rs1, rs2]


class SUB(InstructionR):
    @staticmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        if rd == rs1 or rd == rs2:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        return [rs1, rs2]


class SLL(InstructionR):
    @staticmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        # TODO: Better logic for most R instructions
        if rd == rs1 or rd == rs2:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        return [rs1, rs2]


class SLT(InstructionR):
    @staticmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        if rd == rs1 or rd == rs2:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        return [rs1, rs2]


class SLTU(InstructionR):
    @staticmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        if rd == rs1 or rd == rs2:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        return [rs1, rs2]


class XOR(InstructionR):
    @staticmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        if rd == rs1 or rd == rs2:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        return [rs1, rs2]


class SRL(InstructionR):
    @staticmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        if rd == rs1 or rd == rs2:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        return [rs1, rs2]


class SRA(InstructionR):
    @staticmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        if rd == rs1 or rd == rs2:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        return [rs1, rs2]


class OR(InstructionR):
    @staticmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        if rd == rs1 or rd == rs2:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        return [rs1, rs2]


class AND(InstructionR):
    @staticmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        if rd == rs1 or rd == rs2:
            return []
        else:
            return [rd]

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register]:
        return [rs1, rs2]
