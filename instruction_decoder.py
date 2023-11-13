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
    def encode_injection_intervals(cls, instructions: pd.DataFrame):
        N = len(instructions)
        M = 32
        non_inject = np.zeros((N, M))

        unique_tracker = np.zeros(M)
        override_tracker = np.zeros(M).astype(bool)
        # Muffin Logic
        for _i in tqdm(range(N), colour="green", desc="Instruction", leave=False):
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

        return non_inject

    @classmethod
    def get_injection_times(
        cls, encoded_intervals: pd.DataFrame
    ) -> Tuple[pd.Series, pd.Series]:
        sensitive = dict()
        non_sensitive = dict()

        last_val = -420 * np.ones(32)
        for reg in tqdm(
            encoded_intervals.columns,
            position=0,
            desc="Register",
            colour="green",
            leave=False,
        ):
            for cycle in tqdm(
                encoded_intervals.index,
                position=1,
                desc="Cycle",
                colour="green",
                leave=False,
            ):
                if encoded_intervals[reg][cycle] == last_val[reg]:
                    continue

                if encoded_intervals[reg][cycle] == 0:
                    non_sensitive[cycle] = reg
                else:
                    sensitive[cycle] = reg

                last_val[reg] = encoded_intervals[reg][cycle]

        return pd.Series(sensitive), pd.Series(non_sensitive)
