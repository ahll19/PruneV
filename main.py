import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from instruction_decoder import InstructionDecoder


def prep() -> pd.DataFrame:
    path = "golden_trace.log"

    with open(path, "r") as f:
        lines = f.readlines()

    # header and footer have length 6
    header = [x.strip() for x in lines.pop(0).split("\t")]
    footer = [x.strip() for x in lines.pop(-1).split("\t")]

    # When we split by len \t we get 7 elements. We concatenate the last two
    for i, line in enumerate(lines):
        new_line = line.split("\t")
        new_line = [x.strip() for x in new_line]
        last_element = new_line.pop(-1).strip()
        new_line[-1] += " " + last_element

        lines[i] = new_line

    return pd.DataFrame(lines, columns=header)


if __name__ == "__main__":
    mpl.use("TkAgg")
    df = prep()
    print("Encoding golden core trace")
    tmp = InstructionDecoder.encode_injection_intervals(df)
    print("Done encoding golden core trace")
    print("Parsing unique injection times")
    sensitive, non_sensitive = InstructionDecoder.get_injection_times(tmp)
    print("Done parsing unique injection times")

    sensitive.to_csv("sensitive.csv")
    non_sensitive.to_csv("non_sensitive.csv")

    print(f"Number of sensitive injections: {len(sensitive)}")
    print(f"Number of non-sensitive injections: {len(non_sensitive)}")
    print(
        f"{len(sensitive) * 100 / (len(sensitive) + len(non_sensitive)):.2f}% are sensitive"
    )
