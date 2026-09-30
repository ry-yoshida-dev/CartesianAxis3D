"""Tests for `cartesian_axis.CartesianCoordinateSystem`."""

from __future__ import annotations

import dataclasses

import pytest

from cartesian_axis import (
    Axis,
    AxisOrientation,
    CartesianCoordinateSystem,
    CoordinateHandedness,
    SoftwareCoordinateSystem,
)


@pytest.fixture
def orientation() -> AxisOrientation:
    """An OpenCV-style orientation."""
    return AxisOrientation(forward=Axis.Z, right=Axis.X, up=Axis.Y)


def test_role_properties_delegate_to_orientation(orientation: AxisOrientation) -> None:
    """`forward`, `right`, and `up` come from the axis orientation."""
    system: CartesianCoordinateSystem = CartesianCoordinateSystem(
        coordinate_handedness=CoordinateHandedness.RIGHT,
        axis_orientation=orientation,
    )
    assert system.forward is Axis.Z
    assert system.right is Axis.X
    assert system.up is Axis.Y


@pytest.mark.parametrize(
    ("handedness", "is_right_handed", "is_left_handed"),
    [
        (CoordinateHandedness.RIGHT, True, False),
        (CoordinateHandedness.LEFT, False, True),
    ],
)
def test_handedness_flags_delegate_to_handedness(
    orientation: AxisOrientation,
    handedness: CoordinateHandedness,
    is_right_handed: bool,
    is_left_handed: bool,
) -> None:
    """Handedness flags come from the coordinate handedness."""
    system: CartesianCoordinateSystem = CartesianCoordinateSystem(
        coordinate_handedness=handedness,
        axis_orientation=orientation,
    )
    assert system.is_right_handed is is_right_handed
    assert system.is_left_handed is is_left_handed


@pytest.mark.parametrize(
    "field_name",
    [field.name for field in dataclasses.fields(CartesianCoordinateSystem)],
)
def test_is_frozen(orientation: AxisOrientation, field_name: str) -> None:
    """Coordinate system fields cannot be reassigned after construction."""
    system: CartesianCoordinateSystem = CartesianCoordinateSystem(
        coordinate_handedness=CoordinateHandedness.RIGHT,
        axis_orientation=orientation,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(system, field_name, None)


def test_equality_is_value_based(orientation: AxisOrientation) -> None:
    """Two systems built from equal parts compare equal and hash equally."""
    first: CartesianCoordinateSystem = CartesianCoordinateSystem(
        coordinate_handedness=CoordinateHandedness.RIGHT,
        axis_orientation=orientation,
    )
    second: CartesianCoordinateSystem = CartesianCoordinateSystem(
        coordinate_handedness=CoordinateHandedness.RIGHT,
        axis_orientation=AxisOrientation(forward=Axis.Z, right=Axis.X, up=Axis.Y),
    )
    assert first == second
    assert hash(first) == hash(second)


def test_str_includes_components(orientation: AxisOrientation) -> None:
    """`str` names the class and both components."""
    system: CartesianCoordinateSystem = CartesianCoordinateSystem(
        coordinate_handedness=CoordinateHandedness.RIGHT,
        axis_orientation=orientation,
    )
    text: str = str(system)
    assert text.startswith("CartesianCoordinateSystem(")
    assert str(CoordinateHandedness.RIGHT) in text
    assert str(orientation) in text


def test_get_converting_indices_delegates_to_orientation(
    orientation: AxisOrientation,
) -> None:
    """Conversion indices match those of the underlying orientation."""
    system: CartesianCoordinateSystem = CartesianCoordinateSystem(
        coordinate_handedness=CoordinateHandedness.RIGHT,
        axis_orientation=orientation,
    )
    assert system.get_converting_indices(
        software_coordinate_system=SoftwareCoordinateSystem.PLOTLY
    ) == orientation.get_converting_indices(
        software_coordinate_system=SoftwareCoordinateSystem.PLOTLY
    )
