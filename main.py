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
    vulnerable_registers = [0, 3, 4]

    core_trace_parser = CoreTraceParser(
        ins_lib,
        vulnerable_registers=vulnerable_registers,
        cycle_offset=0,
        ignore_unknown_instructions=True,
        custom_line_parser=custom_line_parser,
    )
    result = core_trace_parser.parse("golden_trace.log")

    n = result.size
    n_non_zero_duplicates = 0
    n_zero = (result == 0).sum().sum()
    for col in result:
        vals = result[col][result[col] != 0]
        n_non_zero_duplicates += vals.duplicated().sum()

    p1 = n_zero / n
    p2 = n_non_zero_duplicates / n
    p3 = p1 + p2

    n_sensitive = (result != 0).sum().sum()
    n_non_sensitive = (result == 0).sum().sum()

    print(f"Zero injections represent: {100*p1:.2f}% of the space")
    print(f"Redundant injections represent: {100*p2:.2f}% of the space")
    print(f"Toal reduction: {100*p3:.2f}%")

    print(f"n={n}")
    print(f"n_0={n_zero}")
    print(f"n_non_zero={n_non_zero_duplicates}")
    print()

    print(f"{100 * n_sensitive / n:.2f}% of the space is sensitive")
    print(f"{100 * n_non_sensitive / n:.2f}% of the space is non-sensitive")

    result.to_csv("golden_trace_encoding.csv")
