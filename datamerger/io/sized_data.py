from dataclasses import dataclass

import numpy as np


@dataclass
class SizedData:
    """A two-dimensional array of data with a physical size.

    Each element is assumed to be square, so only one size need be recorded.
    """

    # The array of data.
    data: np.ndarray

    # The size of each element in µm.
    element_size: float
