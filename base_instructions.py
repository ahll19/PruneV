from abc import ABC, abstractmethod
from typing import List

from register import Register


class Instruction(ABC):
    @staticmethod
    @abstractmethod
    def overrides() -> List[Register] | None:
        pass

    @staticmethod
    @abstractmethod
    def reads() -> List[Register] | None:
        pass

    @staticmethod
    @abstractmethod
    def format() -> str:
        pass


class InstructionUJ(Instruction):
    format = "UJ"

    @staticmethod
    @abstractmethod
    def overrides(rd: Register, imm: int) -> List[Register] | None:
        pass

    @staticmethod
    def reads(rd: Register, imm: int) -> List[Register] | None:
        pass


class InstructionI(Instruction):
    format = "I"

    @staticmethod
    @abstractmethod
    def overrides(rd: Register, rs1: Register, imm: int) -> List[Register] | None:
        pass

    @staticmethod
    def reads(rd: Register, rs1: Register, imm: int) -> List[Register] | None:
        pass


class InstructionB(Instruction):
    format = "B"

    @staticmethod
    @abstractmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register] | None:
        pass

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register] | None:
        pass


class InstructionS(Instruction):
    format = "S"

    @staticmethod
    @abstractmethod
    def overrides(rs1: Register, rs2: Register, imm: int) -> List[Register] | None:
        pass

    @staticmethod
    def reads(rs1: Register, rs2: Register, imm: int) -> List[Register] | None:
        pass


class InstructionR(Instruction):
    format = "R"

    @staticmethod
    @abstractmethod
    def overrides(rd: Register, rs1: Register, rs2: Register) -> List[Register] | None:
        pass

    @staticmethod
    def reads(rd: Register, rs1: Register, rs2: Register) -> List[Register] | None:
        pass
