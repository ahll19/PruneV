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
    ) -> Tuple[List[Register] | None, List[Register] | None]:
        instr, kwargs = InstructionFormatter.format(instruction, memory_content)

        if instr is None or kwargs is None:
            return None, None

        overrides = instr.overrides(**kwargs)
        reads = instr.reads(**kwargs)

        return overrides, reads

    @classmethod
    def injection_coverage(cls, instructions: pd.DataFrame):
        _ = ""

        N = len(instructions)
        register_map = {Register(i): i for i in range(32)}
        coverage = np.zeros((32, N))
        worth_injecting = np.ones(32)

        print("Calculating injection coverage... ")

        for _i in tqdm(range(N)):
            i = N - _i - 1
            row = instructions.iloc[i]

            instr = row["Decoded instruction"]
            mem_cont = row["Register and memory contents"]
            overrides, reads = cls.override_read_results(instr, mem_cont)

            if overrides is not None:
                over_idx = [register_map[r] for r in overrides]
            else:
                over_idx = []

            if reads is not None:
                read_idx = [register_map[r] for r in reads]
            else:
                read_idx = []

            for idx in over_idx:
                worth_injecting[idx] = 0

            for idx in read_idx:
                worth_injecting[idx] = 1

            coverage[:, i] = worth_injecting

        tmp = np.sum(coverage) * 100 / (N * 32)
        print(f"Reduced space to {tmp:.2f}% of original")
        print(f"Cut away {100 - tmp:.2f}% of original")
