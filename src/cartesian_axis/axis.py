from __future__ import annotations
import numpy as np
from enum import Enum
from numpy.typing import NDArray

class Axis(Enum):
    """
    Enum defining the three axes (X, Y, Z) in a 3D coordinate system.
    
    Attributes:
    ----------
    X: str
        X-axis.
    Y: str
        Y-axis.
    Z: str
        Z-axis.
    """
    X = "X"
    Y = "Y"
    Z = "Z"

    @property
    def other_axes(self) -> tuple[Axis, Axis]:
        """
        Get the other axes.

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
        Get the index of the axis.

        Returns
        -------
        int
            The index of the axis.
        """
        match self:
            case Axis.X:
                return 0
            case Axis.Y:
                return 1
            case Axis.Z:
                return 2

    @classmethod
    def from_index(
        cls, 
        index: int
        ) -> Axis:
        """
        Get the axis from the index.

        Parameters
        ----------
        index: int
            The index of the axis.

        Returns
        -------
        Axis
            The axis.
        """
        match index:
            case 0:
                return Axis.X
            case 1:
                return Axis.Y
            case 2:
                return Axis.Z
            case _:
                raise ValueError(f"Invalid index: {index}")

    @property
    def unit_vector(self) -> NDArray[np.float64]:
        """
        Get the unit vector of the axis.
        
        Returns
        -------
        np.ndarray
            The unit vector of the axis.
        """
        match self:
            case Axis.X:
                return np.array([1.0, 0.0, 0.0], dtype=np.float64)
            case Axis.Y:
                return np.array([0.0, 1.0, 0.0], dtype=np.float64)
            case Axis.Z:
                return np.array([0.0, 0.0, 1.0], dtype=np.float64)


    

if __name__ == "__main__":
    axis = Axis.X
    print(f"axis.other_axes: {axis.other_axes}")
    print(f"axis.to_index: {axis.to_index}")
    axis = Axis.from_index(0)
    print(f"axis: {axis}")