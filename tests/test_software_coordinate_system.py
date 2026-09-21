import numpy as np

from cartesian_axis import (
    AxisOrientation,
    CartesianCoordinateSystem,
    CoordinateHandedness,
    SoftwareCoordinateSystem,
)


class TestSoftwareCoordinateSystem:
    """Tests for SoftwareCoordinateSystem."""

    def test_all_members_define_coordinate_system(self) -> None:
        for software_coordinate_system in SoftwareCoordinateSystem:
            assert isinstance(
                software_coordinate_system.coordinate_system, CartesianCoordinateSystem
            )

    def test_unity_and_opencv_differ_only_in_handedness(self) -> None:
        unity: CartesianCoordinateSystem = (
            SoftwareCoordinateSystem.UNITY.coordinate_system
        )
        opencv: CartesianCoordinateSystem = (
            SoftwareCoordinateSystem.OPENCV.coordinate_system
        )
        assert unity.axis_orientation == opencv.axis_orientation
        assert unity.is_left_handed
        assert opencv.is_right_handed

    def test_positive_axes_of_z_up_systems_match_handedness(self) -> None:
        for software_coordinate_system in (
            SoftwareCoordinateSystem.BLENDER,
            SoftwareCoordinateSystem.AUTOCAD,
            SoftwareCoordinateSystem.UNREAL_ENGINE,
        ):
            orientation: AxisOrientation = software_coordinate_system.axis_orientation
            triple_product: float = float(
                np.dot(
                    np.cross(
                        orientation.right.unit_vector, orientation.forward.unit_vector
                    ),
                    orientation.up.unit_vector,
                )
            )
            is_right_handed: bool = triple_product > 0
            assert is_right_handed == (
                software_coordinate_system.coordinate_handedness
                == CoordinateHandedness.RIGHT
            )
