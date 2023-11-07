import pandas as pd
import numpy as np
from tqdm import tqdm

from register import Register
from instruction_formatter import InstructionFormatter

from typing import List, Tuple


class InstructionDecoder:
    @classmethod
    def override_read_results(
        cls, instruction: str, memory_content: str
    ) -> Tuple[List[Register], List[Register]]:
        instr, kwargs = InstructionFormatter.format(instruction, memory_content)

        if instr is None or kwargs is None:
            return [], []

        overrides = instr.overrides(**kwargs)
        reads = instr.reads(**kwargs)

        return overrides, reads

    @classmethod
    def injection_coverage(cls, instructions: pd.DataFrame):
        N = len(instructions)
        M = 32
        non_inject = np.zeros((N, M))

        unique_tracker = np.zeros(M)
        override_tracker = np.zeros(M).astype(bool)
        # Muffin Logic
        for _i in tqdm(range(N)):
            i = N - _i - 1
            row = instructions.iloc[i]

            instr = row["Decoded instruction"]
            mem_cont = row["Register and memory contents"]
            overrides, reads = cls.override_read_results(instr, mem_cont)

            for read in reads:
                unique_tracker[read.id] += 1
                override_tracker[read.id] = False

            for override in overrides:
                override_tracker[override.id] = True

            non_inject[i] = unique_tracker
            non_inject[i][override_tracker] = 0

        non_inject = pd.DataFrame(non_inject, index=instructions["Cycle"])

        _ = ""
