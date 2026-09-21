import numpy as np
import pytest

from cartesian_axis import Axis, AxisName, AxisOrientation, SoftwareCoordinateSystem


class TestAxisOrientation:
    """Tests for AxisOrientation."""

    def test_duplicate_axes_raise(self) -> None:
        with pytest.raises(ValueError, match="must be different"):
            AxisOrientation(forward=Axis.X, right=Axis.X, up=Axis.Z)

    def test_get_axis_and_axis_name_are_inverse(self) -> None:
        orientation: AxisOrientation = AxisOrientation(
            forward=Axis.Z, right=Axis.X, up=Axis.Y
        )
        for axis_name in AxisName:
            assert (
                orientation.get_axis_name(orientation.get_axis(axis_name)) == axis_name
            )

    def test_unit_vector_is_float(self) -> None:
        orientation: AxisOrientation = AxisOrientation(
            forward=Axis.Z, right=Axis.X, up=Axis.Y
        )
        assert orientation.unit_vector.dtype == np.float64
        np.testing.assert_array_equal(
            orientation.unit_vector, [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
        )

    def test_converting_indices_to_plotly(self) -> None:
        source: AxisOrientation = SoftwareCoordinateSystem.OPENCV.axis_orientation
        indices: tuple[int, int, int] = source.get_converting_indices(
            software_coordinate_system=SoftwareCoordinateSystem.PLOTLY
        )
        assert indices == (source.forward.to_index, source.right.to_index, 1)
        assert indices == (2, 0, 1)

    def test_converting_indices_preserve_roles(self) -> None:
        for source_system in SoftwareCoordinateSystem:
            for target_system in SoftwareCoordinateSystem:
                source: AxisOrientation = source_system.axis_orientation
                target: AxisOrientation = target_system.axis_orientation
                indices: tuple[int, int, int] = source.get_converting_indices(
                    software_coordinate_system=target_system
                )
                for target_axis in Axis:
                    source_axis: Axis = Axis.from_index(indices[target_axis.to_index])
                    assert source.get_axis_name(source_axis) == target.get_axis_name(
                        target_axis
                    )
