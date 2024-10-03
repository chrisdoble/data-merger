import numpy as np


def load(path: str, placeholder: float) -> np.ndarray:
    """Loads profilometer data.

    Sometimes values in the file are equal to the most negative 32-bit float. I
    don't know why, but they're not valid measurements. They will be replaced
    with the `placeholder` parameter.

    :param path: The path to the profilometer data.
    :param placeholder: If values in the file are equal to the most negative
        32-bit float they will be replaced with this value.
    """
    with open(path) as f:
        lines = f.read().splitlines()
        assert len(lines) >= 4, "Too few lines in profilometer data"
        return np.array(
            [
                [
                    placeholder if s == "-3.4028235E+38" else float(s)
                    for s in line.split("\t")
                ]
                for line in lines[3:]
            ]
        )
