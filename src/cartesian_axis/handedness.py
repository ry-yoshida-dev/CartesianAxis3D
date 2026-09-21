from __future__ import annotations

from enum import Enum


class CoordinateHandedness(Enum):
    """
    Enum defining the coordinate handedness.

    With the hand of this handedness, the thumb, index finger, and middle
    finger point along the positive X, Y, and Z axes respectively.

    Attributes
    ----------
    RIGHT : str
        Right-handed coordinate system.
    LEFT : str
        Left-handed coordinate system.
    """

    RIGHT = "right"
    LEFT = "left"

    @property
    def is_right_handed(self) -> bool:
        """
        Check if the coordinate handedness is right-handed.

        Returns
        -------
        bool
            True if the coordinate handedness is right-handed, False otherwise.
        """
        return self == CoordinateHandedness.RIGHT

    @property
    def is_left_handed(self) -> bool:
        """
        Check if the coordinate handedness is left-handed.

        Returns
        -------
        bool
            True if the coordinate handedness is left-handed, False otherwise.
        """
        return self == CoordinateHandedness.LEFT

    @property
    def cross_product_value(self) -> int:
        """
        Get the sign applied to cross products in this handedness.

        Returns
        -------
        int
            1 for right-handed and -1 for left-handed.
        """
        match self:
            case CoordinateHandedness.RIGHT:
                return 1
            case CoordinateHandedness.LEFT:
                return -1
