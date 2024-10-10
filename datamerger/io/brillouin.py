import numpy as np
import pandas as pd

from .sized_data import SizedData


def load(path: str) -> SizedData:
    """Loads Brillouin data from an Excel spreadsheet.

    Each element is assumed to have a size of 50µm.

    :param path: The path to the Brillouin data.
    :return: The Brillouin data contained within the file at `path`.
    """
    return SizedData(pd.read_excel(path, dtype=np.float32, header=None).to_numpy(), 50)
