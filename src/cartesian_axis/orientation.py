import numpy as np
from dataclasses import dataclass
from typing import TYPE_CHECKING
from numpy.typing import NDArray
from .axis import Axis

if TYPE_CHECKING:
    from .software_coordinate_system import SoftwareCoordinateSystem

@dataclass(frozen=True)
class AxisOrientation:
    """
    A class representing the orientation of the axes.

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
    forward: Axis
        The forward axis.
    right: Axis
        The right axis.
    up: Axis
        The up axis.
    """
    forward: Axis
    right: Axis
    up: Axis

    def __post_init__(self) -> None:
        self.validate_axis_orientation()

    def get_converting_indices(
        self, 
        software_coordinate_system: "SoftwareCoordinateSystem"
        ) -> tuple[int, int, int]:
        """
        This method aligns axis indices when mapping data between different conventions. 
        For example, it handles the transformation of coordinate data stored in a Z-up system for visualization in a Y-up environment (such as Plotly), 
        ensuring each axis is correctly indexed.

        Parameters
        ----------
        software_coordinate_system: SoftwareCoordinateSystem
            The software coordinate system to convert to.

        Returns
        -------
        tuple[int, int, int]:
            The indices of the axes in the other software coordinate system.
        """
        from .software_coordinate_system import SoftwareCoordinateSystem
        match software_coordinate_system:
            case SoftwareCoordinateSystem.PLOTLY:
                return (self.forward.to_index, self.right.to_index ,self.up.to_index)
            case _:
                raise NotImplementedError("Not implemented")

    @property
    def is_y_up(self) -> bool:
        return self.up == Axis.Y
    
    @property
    def is_z_up(self) -> bool:
        return self.up == Axis.Z

    @property
    def is_x_up(self) -> bool:
        return self.up == Axis.X

    @property
    def unit_vector(self) -> NDArray[np.float64]:
        """
        The stack of unit vectors in the forward, right, and up directions.
        
        Returns
        -------
        np.ndarray:
            The unit vectors of the axes.
        """
        return np.array([self.forward.unit_vector, self.right.unit_vector, self.up.unit_vector])

    def validate_axis_orientation(self) -> None:
        values = [self.forward.value, self.right.value, self.up.value]
        if len(set(values)) != 3:
            raise ValueError(f"Forward, right, and up axes must be different.\
            \nforward: {self.forward}, \
            \nright: {self.right}, \
            \nup: {self.up}")
