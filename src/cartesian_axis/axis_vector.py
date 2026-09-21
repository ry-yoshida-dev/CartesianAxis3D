from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .axis import Axis


@dataclass(init=False, eq=False)
class AxisVectors:
    """
    Vectors of shape (3,) associated with the X, Y, and Z axes.

    The inputs are copied and converted to float64 arrays. Two instances are
    equal when all of their vectors are element-wise equal.

    Parameters
    ----------
    x : ArrayLike
        The vector for the X axis.
    y : ArrayLike
        The vector for the Y axis.
    z : ArrayLike
        The vector for the Z axis.

    Raises
    ------
    ValueError
        If any vector does not have shape (3,).
    """

    x: NDArray[np.float64]
    y: NDArray[np.float64]
    z: NDArray[np.float64]

    def __init__(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> None:
        self.x = self._to_vector(x)
        self.y = self._to_vector(y)
        self.z = self._to_vector(z)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AxisVectors):
            return NotImplemented
        return bool(
            np.array_equal(self.x, other.x)
            and np.array_equal(self.y, other.y)
            and np.array_equal(self.z, other.z)
        )

    @staticmethod
    def _to_vector(vector: ArrayLike) -> NDArray[np.float64]:
        converted_vector: NDArray[np.float64] = np.array(vector, dtype=np.float64)
        if converted_vector.shape != (3,):
            raise ValueError(
                f"Vector must have shape (3,), got {converted_vector.shape}"
            )
        return converted_vector

    def get(self, axis: Axis) -> NDArray[np.float64]:
        """
        Get the vector for the given axis.

        Parameters
        ----------
        axis : Axis
            The axis.

        Returns
        -------
        NDArray[np.float64]
            The vector associated with the axis.
        """
        match axis:
            case Axis.X:
                return self.x
            case Axis.Y:
                return self.y
            case Axis.Z:
                return self.z

    def register(self, axis: Axis, vector: ArrayLike) -> None:
        """
        Register the vector for the given axis.

        Parameters
        ----------
        axis : Axis
            The axis.
        vector : ArrayLike
            The vector of shape (3,).

        Raises
        ------
        ValueError
            If the vector does not have shape (3,).
        """
        converted_vector: NDArray[np.float64] = self._to_vector(vector)
        match axis:
            case Axis.X:
                self.x = converted_vector
            case Axis.Y:
                self.y = converted_vector
            case Axis.Z:
                self.z = converted_vector

    def to_array(self) -> NDArray[np.float64]:
        """
        Stack the vectors into a 3x3 array.

        Returns
        -------
        NDArray[np.float64]
            Vectors stacked as rows in X/Y/Z order.
        """
        return np.stack([self.x, self.y, self.z], axis=0)

    @classmethod
    def zero_vectors(cls) -> AxisVectors:
        """
        Create zero vectors for all axes.

        Returns
        -------
        AxisVectors
            The zero axis vectors.
        """
        return cls(
            x=np.zeros(3, dtype=np.float64),
            y=np.zeros(3, dtype=np.float64),
            z=np.zeros(3, dtype=np.float64),
        )

    @classmethod
    def from_array(cls, array: ArrayLike) -> AxisVectors:
        """
        Create axis vectors from a 3x3 array whose rows are in X/Y/Z order.

        Parameters
        ----------
        array : ArrayLike
            The array of shape (3, 3).

        Returns
        -------
        AxisVectors
            The axis vectors.

        Raises
        ------
        ValueError
            If the array does not have shape (3, 3).
        """
        converted_array: NDArray[np.float64] = np.array(array, dtype=np.float64)
        if converted_array.shape != (3, 3):
            raise ValueError(
                f"Array must have shape (3, 3), got {converted_array.shape}"
            )
        return cls(
            x=converted_array[0, :], y=converted_array[1, :], z=converted_array[2, :]
        )
