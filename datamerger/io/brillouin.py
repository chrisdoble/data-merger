import numpy as np
import pandas as pd


def load(path: str) -> np.ndarray:
    """Loads Brillouin data from an Excel spreadsheet.

    :param path: The path to the Brillouin data.
    :return: The Brillouin data contained within the file as `path`.
    """
    return pd.read_excel(path, dtype=np.float32, header=None).to_numpy()
