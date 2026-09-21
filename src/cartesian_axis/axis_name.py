from __future__ import annotations

from enum import Enum


class AxisName(Enum):
    """
    Enum defining the semantic roles of the axes.

    Attributes
    ----------
    FORWARD : str
        Forward axis.
    RIGHT : str
        Right axis.
    UP : str
        Up axis.
    """

    FORWARD = "forward"
    RIGHT = "right"
    UP = "up"

    @property
    def other_axes(self) -> tuple[AxisName, AxisName]:
        """
        Get the other two axis roles.

        Returns
        -------
        tuple[AxisName, AxisName]
            The other axis roles.
        """
        match self:
            case AxisName.FORWARD:
                return (AxisName.RIGHT, AxisName.UP)
            case AxisName.RIGHT:
                return (AxisName.FORWARD, AxisName.UP)
            case AxisName.UP:
                return (AxisName.FORWARD, AxisName.RIGHT)
