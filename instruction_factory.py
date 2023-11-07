from base_instructions import Instruction
from instructions import (
    LUI,
    AUIPC,
    JAL,
    JALR,
    BEQ,
    BNE,
    BLT,
    BGE,
    BLTU,
    BGEU,
    LB,
    LH,
    LW,
    LBU,
    LHU,
    SB,
    SH,
    SW,
    ADDI,
    SLTI,
    SLTIU,
    XORI,
    ORI,
    ANDI,
    SLLI,
    SRLI,
    SRAI,
    ADD,
    SUB,
    SLL,
    SLT,
    SLTU,
    XOR,
    SRL,
    SRA,
    OR,
    AND,
)


class InstructionFactory:
    instruction_map = {
        "LUI": LUI,
        "AUIPC": AUIPC,
        "JAL": JAL,
        "JALR": JALR,
        "BEQ": BEQ,
        "BNE": BNE,
        "BLT": BLT,
        "BGE": BGE,
        "BLTU": BLTU,
        "BGEU": BGEU,
        "LB": LB,
        "LH": LH,
        "LW": LW,
        "LBU": LBU,
        "LHU": LHU,
        "SB": SB,
        "SH": SH,
        "SW": SW,
        "ADDI": ADDI,
        "SLTI": SLTI,
        "SLTIU": SLTIU,
        "XORI": XORI,
        "ORI": ORI,
        "ANDI": ANDI,
        "SLLI": SLLI,
        "SRLI": SRLI,
        "SRAI": SRAI,
        "ADD": ADD,
        "SUB": SUB,
        "SLL": SLL,
        "SLT": SLT,
        "SLTU": SLTU,
        "XOR": XOR,
        "SRL": SRL,
        "SRA": SRA,
        "OR": OR,
        "AND": AND,
    }

    @classmethod
    def get_instruction(cls, instr: str) -> Instruction | None:
        try:
            return cls.instruction_map[instr.upper()]
        except:
            return None

    @classmethod
    def get_instruction_format(cls, instr: str) -> str:
        return cls.get_instruction(instr).format
