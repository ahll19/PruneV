# Change the line below to your own decoder if you want to customize the parser.
from .line_and_decoders.ibex_line_decoder import IbexLineDecoder as LineDecoder

from .line_and_decoders.line import Line
from .instructions.instruction_factory import InstructionLibrary, InstructionFactory
from .register import Register

from typing import List, Tuple

import numpy as np
import pandas as pd
from tqdm import tqdm


class CoreTraceParser:
    instruction_library: InstructionLibrary = None
    trace_has_footer: bool = None
    n_registers: int = None
    vulnerable_registers: List[int] = None
    ignore_unknown_instructions: bool = None
    custom_line_parser: callable = None

    line_decoder: LineDecoder = None

    def __init__(
        self,
        instruction_library: InstructionLibrary,
        trace_has_footer: bool = True,
        n_registers: int = 32,
        vulnerable_registers: List[int] = [],
        ignore_unknown_instructions: bool = False,
        custom_line_parser: callable = None,
    ) -> None:
        self.instruction_library = instruction_library
        self.trace_has_footer = trace_has_footer
        self.n_registers = n_registers
        self.vulnerable_registers = vulnerable_registers
        self.ignore_unknown_instructions = ignore_unknown_instructions
        self.custom_line_parser = custom_line_parser

    def parse(self, path: str) -> pd.DataFrame:
        with open(path, "r") as f:
            lines = f.readlines()

        header = lines.pop(0)
        footer = lines.pop(-1) if self.trace_has_footer else None
        self.line_decoder = LineDecoder(header, footer)

        decoded_lines = []
        reads = []
        overrides = []

        for line in tqdm(lines, desc="Parsing lines", leave=True):
            if self.ignore_unknown_instructions:
                _a, _b, _c = self._parse_line_ign(line)
            else:
                _a, _b, _c = self._parse_line_not_ign(line)

            reads.append(_a)
            overrides.append(_b)
            decoded_lines.append(_c)

        # sorts the list according to the first value of the line objects (i.e. cycle)
        decoded_lines, reads, overrides = zip(
            *sorted(zip(decoded_lines, reads, overrides))
        )

        start_cycle = decoded_lines[0].cycle
        end_cycle = decoded_lines[-1].cycle

        unique_injection_interval_tracker = np.zeros(self.n_registers, dtype=int)
        override_tracker = np.zeros(self.n_registers).astype(bool)
        result = np.zeros((end_cycle, self.n_registers), dtype=int) * np.nan

        indexer = len(decoded_lines) - 1
        read = list()
        override = list()
        for _i in tqdm(range(end_cycle), desc="Encoding inject intervals", leave=True):
            i = end_cycle - _i - 1

            if i + 1 == decoded_lines[indexer].cycle:
                read = reads[indexer]
                override = overrides[indexer]
                indexer -= 1

            result[i][override_tracker] = 0

            for r in read:
                unique_injection_interval_tracker[r.id] += 1
                override_tracker[r.id] = False
            for o in override:
                override_tracker[o.id] = True

            result[i] = unique_injection_interval_tracker

        for reg in self.vulnerable_registers:
            result[:, reg] = np.arange(1, end_cycle + 1)

        result = result.astype(int)
        result = result[start_cycle:]

        columns = [f"x{i}" for i in range(self.n_registers)]
        index = pd.Index(range(start_cycle, end_cycle), name="Cycle")
        result = pd.DataFrame(result, columns=columns, index=index)

        return result

    def _parse_line_ign(self, line: str) -> Tuple[List[Register], List[Register], Line]:
        try:
            return self._parse_line_not_ign(line)
        except AttributeError:
            return self.custom_line_parser(line)

    def _parse_line_not_ign(
        self, line: str
    ) -> Tuple[List[Register], List[Register], Line]:
        decoded_line = self.line_decoder.decode_line(line)
        instr = InstructionFactory.get_instruction(
            self.instruction_library, decoded_line.instruction
        )
        reads = instr.reads(**decoded_line.instruction_kwargs)
        overrides = instr.overrides(**decoded_line.instruction_kwargs)

        return reads, overrides, decoded_line
