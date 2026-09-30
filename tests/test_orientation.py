"""Tests for `cartesian_axis.AxisOrientation`."""

from __future__ import annotations

import dataclasses
import itertools

import numpy as np
import pytest

from cartesian_axis import Axis, AxisOrientation, SoftwareCoordinateSystem

VALID_PERMUTATIONS: list[tuple[Axis, ...]] = list(itertools.permutations(Axis))


@pytest.mark.parametrize(("forward", "right", "up"), VALID_PERMUTATIONS)
def test_accepts_every_axis_permutation(forward: Axis, right: Axis, up: Axis) -> None:
    """Any assignment of three distinct axes is a valid orientation."""
    orientation: AxisOrientation = AxisOrientation(forward=forward, right=right, up=up)
    assert (orientation.forward, orientation.right, orientation.up) == (
        forward,
        right,
        up,
    )


@pytest.mark.parametrize(
    ("forward", "right", "up"),
    [
        (Axis.X, Axis.X, Axis.Z),
        (Axis.X, Axis.Y, Axis.X),
        (Axis.Z, Axis.Y, Axis.Y),
        (Axis.Y, Axis.Y, Axis.Y),
    ],
)
def test_rejects_duplicated_axes(forward: Axis, right: Axis, up: Axis) -> None:
    """Construction fails fast when any two roles share an axis."""
    with pytest.raises(ValueError, match="must be different"):
        _ = AxisOrientation(forward=forward, right=right, up=up)


@pytest.mark.parametrize(
    "field_name", [field.name for field in dataclasses.fields(AxisOrientation)]
)
def test_is_frozen(field_name: str) -> None:
    """Orientation fields cannot be reassigned after construction."""
    orientation: AxisOrientation = AxisOrientation(
        forward=Axis.X, right=Axis.Y, up=Axis.Z
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(orientation, field_name, Axis.X)


@pytest.mark.parametrize(
    ("up", "is_x_up", "is_y_up", "is_z_up"),
    [
        (Axis.X, True, False, False),
        (Axis.Y, False, True, False),
        (Axis.Z, False, False, True),
    ],
)
def test_up_axis_flags(up: Axis, is_x_up: bool, is_y_up: bool, is_z_up: bool) -> None:
    """Exactly one `is_*_up` flag matches the `up` axis."""
    forward, right = up.other_axes
    orientation: AxisOrientation = AxisOrientation(forward=forward, right=right, up=up)
    assert orientation.is_x_up is is_x_up
    assert orientation.is_y_up is is_y_up
    assert orientation.is_z_up is is_z_up


def test_unit_vector_stacks_forward_right_up() -> None:
    """`unit_vector` rows are the forward, right, and up unit vectors."""
    orientation: AxisOrientation = AxisOrientation(
        forward=Axis.Z, right=Axis.X, up=Axis.Y
    )
    expected = np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ]
    )
    np.testing.assert_array_equal(orientation.unit_vector, expected)


def test_unit_vector_is_float64() -> None:
    """`unit_vector` has the float64 dtype declared in its annotation."""
    orientation: AxisOrientation = AxisOrientation(
        forward=Axis.X, right=Axis.Y, up=Axis.Z
    )
    assert orientation.unit_vector.dtype == np.float64


@pytest.mark.parametrize(("forward", "right", "up"), VALID_PERMUTATIONS)
def test_unit_vector_is_permutation_matrix(
    forward: Axis, right: Axis, up: Axis
) -> None:
    """`unit_vector` is always an orthogonal permutation matrix."""
    orientation: AxisOrientation = AxisOrientation(forward=forward, right=right, up=up)
    matrix = orientation.unit_vector
    np.testing.assert_array_equal(matrix @ matrix.T, np.eye(3))


@pytest.mark.parametrize(
    ("orientation", "expected_indices"),
    [
        (AxisOrientation(forward=Axis.X, right=Axis.Y, up=Axis.Z), (0, 1, 2)),
        (AxisOrientation(forward=Axis.Z, right=Axis.X, up=Axis.Y), (2, 0, 1)),
    ],
)
def test_get_converting_indices_to_plotly(
    orientation: AxisOrientation,
    expected_indices: tuple[int, int, int],
) -> None:
    """Plotly conversion indices are the forward, right, and up axis indices."""
    assert (
        orientation.get_converting_indices(
            software_coordinate_system=SoftwareCoordinateSystem.PLOTLY
        )
        == expected_indices
    )


def test_converting_indices_reorder_points_into_plotly_axes() -> None:
    """Indexing points with the result moves each role onto Plotly's axis."""
    opencv_orientation: AxisOrientation = AxisOrientation(
        forward=Axis.Z, right=Axis.X, up=Axis.Y
    )
    points_in_opencv = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

    indices = opencv_orientation.get_converting_indices(
        software_coordinate_system=SoftwareCoordinateSystem.PLOTLY
    )
    points_in_plotly = points_in_opencv[:, list(indices)]

    plotly_orientation: AxisOrientation = (
        SoftwareCoordinateSystem.PLOTLY.axis_orientation
    )
    np.testing.assert_array_equal(
        points_in_plotly[:, plotly_orientation.forward.to_index],
        points_in_opencv[:, opencv_orientation.forward.to_index],
    )
    np.testing.assert_array_equal(
        points_in_plotly[:, plotly_orientation.right.to_index],
        points_in_opencv[:, opencv_orientation.right.to_index],
    )
    np.testing.assert_array_equal(
        points_in_plotly[:, plotly_orientation.up.to_index],
        points_in_opencv[:, opencv_orientation.up.to_index],
    )


@pytest.mark.parametrize(
    "software_coordinate_system",
    [
        system
        for system in SoftwareCoordinateSystem
        if system is not SoftwareCoordinateSystem.PLOTLY
    ],
)
def test_get_converting_indices_unsupported_target(
    software_coordinate_system: SoftwareCoordinateSystem,
) -> None:
    """Targets other than Plotly are not implemented yet."""
    orientation: AxisOrientation = AxisOrientation(
        forward=Axis.X, right=Axis.Y, up=Axis.Z
    )
    with pytest.raises(NotImplementedError):
        _ = orientation.get_converting_indices(
            software_coordinate_system=software_coordinate_system
        )
