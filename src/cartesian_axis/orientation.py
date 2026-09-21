from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from .axis import Axis
from .axis_name import AxisName

if TYPE_CHECKING:
    from .software_coordinate_system import SoftwareCoordinateSystem


@dataclass(frozen=True)
class AxisOrientation:
    """
    Assignment of the forward, right, and up roles to the X, Y, and Z axes.

    Only which axis carries each role is specified; the positive direction
    of each axis is not. For example, the up axis may be positive downward.

    Each field says which Cartesian axis fills a role. The role names come
    from the Fleming-style finger mnemonic, not from screen or world
    directions: with the thumb, index finger, and middle finger held at right
    angles along the positive axes, the thumb is ``right``, the index finger
    is ``up``, and the middle finger is ``forward``.

    For example, OpenCV is ``right=X, up=Y, forward=Z``: the right hand's
    thumb, index finger, and middle finger lie along +X, +Y, and +Z. +Y
    points toward the bottom of the image, but it is still the ``up`` axis
    under this convention; it must not be renamed to "down" or negated.

    Parameters
    ----------
    forward : Axis
        The forward axis.
    right : Axis
        The right axis.
    up : Axis
        The up axis.

    Raises
    ------
    ValueError
        If the same axis is assigned to more than one role.
    """

    forward: Axis
    right: Axis
    up: Axis

    def __post_init__(self) -> None:
        self.validate_axis_orientation()

    def validate_axis_orientation(self) -> None:
        """
        Validate that each role is assigned to a different axis.

        Raises
        ------
        ValueError
            If the same axis is assigned to more than one role.
        """
        if len({self.forward, self.right, self.up}) != 3:
            message: str = (
                "Forward, right, and up axes must be different: "
                + f"forward={self.forward}, right={self.right}, up={self.up}"
            )
            raise ValueError(message)

    @property
    def is_x_up(self) -> bool:
        """
        Check if the up axis is X.

        Returns
        -------
        bool
            True if the up axis is X, False otherwise.
        """
        return self.up == Axis.X

    @property
    def is_y_up(self) -> bool:
        """
        Check if the up axis is Y.

        Returns
        -------
        bool
            True if the up axis is Y, False otherwise.
        """
        return self.up == Axis.Y

    @property
    def is_z_up(self) -> bool:
        """
        Check if the up axis is Z.

        Returns
        -------
        bool
            True if the up axis is Z, False otherwise.
        """
        return self.up == Axis.Z

    @property
    def unit_vector(self) -> NDArray[np.float64]:
        """
        Stack the positive unit vectors of the forward, right, and up axes.

        Rows follow forward/right/up order. Each row is the positive unit
        vector of the assigned axis, not the physical direction of the role.

        Returns
        -------
        NDArray[np.float64]
            The unit vectors of shape (3, 3).
        """
        return np.stack(
            [self.forward.unit_vector, self.right.unit_vector, self.up.unit_vector]
        )

    def get_axis(self, axis_name: AxisName) -> Axis:
        """
        Get the axis assigned to a role.

        Parameters
        ----------
        axis_name : AxisName
            The role.

        Returns
        -------
        Axis
            The axis carrying the role.
        """
        match axis_name:
            case AxisName.FORWARD:
                return self.forward
            case AxisName.RIGHT:
                return self.right
            case AxisName.UP:
                return self.up

    def get_axis_name(self, axis: Axis) -> AxisName:
        """
        Get the role assigned to an axis.

        Parameters
        ----------
        axis : Axis
            The axis.

        Returns
        -------
        AxisName
            The role carried by the axis.
        """
        if axis == self.forward:
            return AxisName.FORWARD
        if axis == self.right:
            return AxisName.RIGHT
        return AxisName.UP

    def get_converting_indices(
        self, software_coordinate_system: SoftwareCoordinateSystem
    ) -> tuple[int, int, int]:
        """
        Get the indices that reorder coordinates into a software coordinate system.

        Indexing coordinates of this orientation with the result, as in
        ``points[..., indices]``, yields coordinates whose X, Y, and Z carry
        the same roles as in the software coordinate system. Only the axes
        are permuted; no sign flips are applied.

        Parameters
        ----------
        software_coordinate_system : SoftwareCoordinateSystem
            The software coordinate system to convert to.

        Returns
        -------
        tuple[int, int, int]
            The source axis indices for the target X, Y, and Z axes.
        """
        target: AxisOrientation = software_coordinate_system.axis_orientation
        x_index: int = self.get_axis(target.get_axis_name(Axis.X)).to_index
        y_index: int = self.get_axis(target.get_axis_name(Axis.Y)).to_index
        z_index: int = self.get_axis(target.get_axis_name(Axis.Z)).to_index
        return (x_index, y_index, z_index)
