from __future__ import annotations

from enum import Enum

from .axis import Axis
from .coordinate_system import CartesianCoordinateSystem
from .handedness import CoordinateHandedness
from .orientation import AxisOrientation


class SoftwareCoordinateSystem(Enum):
    """
    Enum defining the coordinate system conventions of software tools.

    Attributes
    ----------
    BLENDER : str
        Blender (right-handed, Z-up).
    UNREAL_ENGINE : str
        Unreal Engine (left-handed, Z-up, X-forward).
    UNITY : str
        Unity (left-handed, Y-up, Z-forward).
    AUTOCAD : str
        AutoCAD (right-handed, Z-up).
    PLOTLY : str
        Plotly (right-handed, Z-up, X-forward).
    OPENCV : str
        OpenCV camera coordinates (right-handed, Z-forward).
    """

    BLENDER = "blender"
    UNREAL_ENGINE = "unreal engine"
    UNITY = "unity"
    AUTOCAD = "autocad"
    PLOTLY = "plotly"
    OPENCV = "opencv"

    @property
    def coordinate_system(self) -> CartesianCoordinateSystem:
        """
        Get the coordinate system of the software.

        Returns
        -------
        CartesianCoordinateSystem
            The coordinate system.
        """
        return CartesianCoordinateSystem(
            coordinate_handedness=self.coordinate_handedness,
            axis_orientation=self.axis_orientation,
        )

    @property
    def coordinate_handedness(self) -> CoordinateHandedness:
        """
        Get the coordinate handedness of the software.

        Returns
        -------
        CoordinateHandedness
            The coordinate handedness.
        """
        match self:
            case (
                SoftwareCoordinateSystem.BLENDER
                | SoftwareCoordinateSystem.AUTOCAD
                | SoftwareCoordinateSystem.PLOTLY
                | SoftwareCoordinateSystem.OPENCV
            ):
                return CoordinateHandedness.RIGHT
            case (
                SoftwareCoordinateSystem.UNREAL_ENGINE | SoftwareCoordinateSystem.UNITY
            ):
                return CoordinateHandedness.LEFT

    @property
    def axis_orientation(self) -> AxisOrientation:
        """
        Get the axis orientation of the software.

        Returns
        -------
        AxisOrientation
            The axis orientation.
        """
        match self:
            case SoftwareCoordinateSystem.BLENDER | SoftwareCoordinateSystem.AUTOCAD:
                return AxisOrientation(forward=Axis.Y, right=Axis.X, up=Axis.Z)
            case (
                SoftwareCoordinateSystem.UNREAL_ENGINE | SoftwareCoordinateSystem.PLOTLY
            ):
                return AxisOrientation(forward=Axis.X, right=Axis.Y, up=Axis.Z)
            case SoftwareCoordinateSystem.UNITY | SoftwareCoordinateSystem.OPENCV:
                return AxisOrientation(forward=Axis.Z, right=Axis.X, up=Axis.Y)
