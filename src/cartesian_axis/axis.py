from __future__ import annotations

from enum import Enum

import numpy as np
from numpy.typing import NDArray


class Axis(Enum):
    """
    Enum defining the three axes (X, Y, Z) in a 3D coordinate system.

    Attributes
    ----------
    X : str
        X-axis.
    Y : str
        Y-axis.
    Z : str
        Z-axis.
    """

    X = "X"
    Y = "Y"
    Z = "Z"

    @property
    def other_axes(self) -> tuple[Axis, Axis]:
        """
        Get the other two axes in X/Y/Z order.

        Returns
        -------
        tuple[Axis, Axis]
            The other axes.
        """
        match self:
            case Axis.X:
                return (Axis.Y, Axis.Z)
            case Axis.Y:
                return (Axis.X, Axis.Z)
            case Axis.Z:
                return (Axis.X, Axis.Y)

    @property
    def to_index(self) -> int:
        """
        Get the index of the axis in X/Y/Z order.

        Returns
        -------
        int
            0 for X, 1 for Y, and 2 for Z.
        """
        match self:
            case Axis.X:
                return 0
            case Axis.Y:
                return 1
            case Axis.Z:
                return 2

    @classmethod
    def from_index(cls, index: int) -> Axis:
        """
        Get the axis from its index in X/Y/Z order.

        Parameters
        ----------
        index : int
            The index of the axis.

        Returns
        -------
        Axis
            The axis.

        Raises
        ------
        ValueError
            If the index is not 0, 1, or 2.
        """
        match index:
            case 0:
                return Axis.X
            case 1:
                return Axis.Y
            case 2:
                return Axis.Z
            case _:
                raise ValueError(f"Invalid axis index: {index}")

    @property
    def unit_vector(self) -> NDArray[np.float64]:
        """
        Get the unit vector pointing in the positive direction of the axis.

        Returns
        -------
        NDArray[np.float64]
            The unit vector of shape (3,).
        """
        unit_vector: NDArray[np.float64] = np.zeros(3, dtype=np.float64)
        unit_vector[self.to_index] = 1.0
        return unit_vector
