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
        # Ensure the pixelSize column is present and has units of µm.
        assert f.readline() == "numCols\tnumRows\tpixelSize (um)\n"

        # Determine the dimensions of the data.
        properties = f.readline().strip().split("\t")
        width = int(properties[0])
        height = int(properties[1])
        pixel_size = float(properties[2])

        # Allocate an array large enough to store it.
        data = np.empty((height, width), np.float64)

        # Ignore the next line.
        f.readline()

        # Load the data.
        i = 0
        while True:
            line = f.readline().strip()
            if line == "":
                break

            j = 0
            for s in line.split("\t"):
                data[i, j] = float("nan" if s == "-3.4028235E+38" else s)
                j += 1

            i += 1

        return SizedData(data, pixel_size)
