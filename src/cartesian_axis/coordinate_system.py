from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .axis import Axis
from .handedness import CoordinateHandedness
from .orientation import AxisOrientation

if TYPE_CHECKING:
    from .software_coordinate_system import SoftwareCoordinateSystem


@dataclass(frozen=True)
class CartesianCoordinateSystem:
    """
    A Cartesian coordinate system defined by handedness and axis orientation.

    Parameters
    ----------
    coordinate_handedness : CoordinateHandedness
        The coordinate handedness (right-handed or left-handed).
    axis_orientation : AxisOrientation
        The assignment of the forward, right, and up roles to the X, Y, and Z axes.
    """

    coordinate_handedness: CoordinateHandedness
    axis_orientation: AxisOrientation

    @property
    def forward(self) -> Axis:
        """
        Get the forward axis.

        Returns
        -------
        Axis
            The forward axis.
        """
        return self.axis_orientation.forward

    @property
    def right(self) -> Axis:
        """
        Get the right axis.

        Returns
        -------
        Axis
            The right axis.
        """
        return self.axis_orientation.right

    @property
    def up(self) -> Axis:
        """
        Get the up axis.

        Returns
        -------
        Axis
            The up axis.
        """
        return self.axis_orientation.up

    @property
    def is_right_handed(self) -> bool:
        """
        Check if the coordinate system is right-handed.

        Returns
        -------
        bool
            True if the coordinate system is right-handed, False otherwise.
        """
        return self.coordinate_handedness.is_right_handed

    @property
    def is_left_handed(self) -> bool:
        """
        Check if the coordinate system is left-handed.

        Returns
        -------
        bool
            True if the coordinate system is left-handed, False otherwise.
        """
        return self.coordinate_handedness.is_left_handed

    def __str__(self) -> str:
        """
        Get the string representation of the coordinate system.

        Returns
        -------
        str
            The string representation of the coordinate system.
        """
        return (
            "CartesianCoordinateSystem("
            + f"coordinate_handedness={self.coordinate_handedness}, "
            + f"axis_orientation={self.axis_orientation})"
        )

    def get_converting_indices(
        self, software_coordinate_system: SoftwareCoordinateSystem
    ) -> tuple[int, int, int]:
        """
        Get the indices that reorder coordinates into a software coordinate system.

        Only the axes are permuted; no sign flips are applied.

        Parameters
        ----------
        software_coordinate_system : SoftwareCoordinateSystem
            The software coordinate system to convert to.

        Returns
        -------
        tuple[int, int, int]
            The source axis indices for the target X, Y, and Z axes.
        """
        return self.axis_orientation.get_converting_indices(
            software_coordinate_system=software_coordinate_system
        )
