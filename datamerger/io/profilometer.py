import numpy as np

from .sized_data import SizedData


def load(path: str) -> SizedData:
    """Loads profilometer data.

    Sometimes values in a profilometer data file are equal to the most negative
    32-bit float. They're not valid measurements and are thus replaced with NaN.

    :param path: The path to the profilometer data.
    :return: The profilometer data contained within the file at `path`.
    """
    with open(path) as f:
        lines = f.read().splitlines()

        # Ensure ther are enough lines to be valid profilometer data.
        assert len(lines) >= 4, "Too few lines in profilometer data"

        # Ensure the pixelSize column is present and has units of µm.
        assert lines[0] == "numCols\tnumRows\tpixelSize (um)"

        return SizedData(
            np.array(
                [
                    [
                        float("nan" if s == "-3.4028235E+38" else s)
                        for s in line.split("\t")
                    ]
                    for line in lines[3:]
                ]
            ),
            float(lines[1].split("\t")[2]),
        )
