from src.core_trace_parser import CoreTraceParser
from src.instructions.instruction_factory import InstructionLibrary
from src.register import Register
from src.line_and_decoders.line import Line

from typing import List, Tuple


def custom_line_parser(line: str) -> Tuple[List[Register], List[Register], Line]:
    tab_split = line.split("\t")
    comma_split = tab_split[5].split(",")
    all_regs = [Register(int(reg[1:])) for reg in comma_split if reg.startswith("x")]

    cycle = int(line.split("\t")[1])
    instruction = line.split("\t")[4]
    instruction_kwargs = dict()
    _line = Line(cycle, instruction, instruction_kwargs)

    return all_regs, [], _line


if __name__ == "__main__":
    ins_lib = InstructionLibrary.RISCV

    core_trace_parser = CoreTraceParser(
        ins_lib,
        vulnerable_registers=[0, 3, 4],
        ignore_unknown_instructions=True,
        custom_line_parser=custom_line_parser,
    )
    result = core_trace_parser.parse("golden_trace.log")

    n = result.size
    n_unique = (result.nunique() - 1).sum()
    n_zero = (result == 0).sum().sum()

    p1 = 100 * (n_unique / n)
    p2 = 100 * (n_zero / n)
    p3 = 100 * (1 - ((n_unique + n_zero) / n))

    print(f"Unique injections represent: {p1:.2f}% of the space")
    print(f"Zero injections represent: {p2:.2f}% of the space")
    print(f"Toal reduction: {p3:.2f}%")
