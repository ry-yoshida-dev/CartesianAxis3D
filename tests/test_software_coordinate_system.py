"""Tests for `cartesian_axis.SoftwareCoordinateSystem`."""

from __future__ import annotations

import numpy as np
import pytest

from cartesian_axis import (
    Axis,
    AxisOrientation,
    CartesianCoordinateSystem,
    CoordinateHandedness,
    SoftwareCoordinateSystem,
)

IMPLEMENTED_SYSTEMS: list[SoftwareCoordinateSystem] = [
    SoftwareCoordinateSystem.PLOTLY,
    SoftwareCoordinateSystem.OPENCV,
]


@pytest.mark.parametrize(
    ("software_coordinate_system", "expected_orientation"),
    [
        (
            SoftwareCoordinateSystem.PLOTLY,
            AxisOrientation(forward=Axis.X, right=Axis.Y, up=Axis.Z),
        ),
        (
            SoftwareCoordinateSystem.OPENCV,
            AxisOrientation(forward=Axis.Z, right=Axis.X, up=Axis.Y),
        ),
    ],
)
def test_axis_orientation(
    software_coordinate_system: SoftwareCoordinateSystem,
    expected_orientation: AxisOrientation,
) -> None:
    """Each implemented software maps to its documented orientation."""
    assert software_coordinate_system.axis_orientation == expected_orientation


@pytest.mark.parametrize(
    ("software_coordinate_system", "expected_handedness"),
    [
        (SoftwareCoordinateSystem.PLOTLY, CoordinateHandedness.RIGHT),
        (SoftwareCoordinateSystem.OPENCV, CoordinateHandedness.RIGHT),
        (SoftwareCoordinateSystem.BLENDER, CoordinateHandedness.RIGHT),
    ],
)
def test_coordinate_handedness(
    software_coordinate_system: SoftwareCoordinateSystem,
    expected_handedness: CoordinateHandedness,
) -> None:
    """Each software with known handedness reports it."""
    assert software_coordinate_system.coordinate_handedness is expected_handedness


@pytest.mark.parametrize("software_coordinate_system", IMPLEMENTED_SYSTEMS)
def test_coordinate_system_combines_handedness_and_orientation(
    software_coordinate_system: SoftwareCoordinateSystem,
) -> None:
    """`coordinate_system` bundles the handedness and orientation properties."""
    system: CartesianCoordinateSystem = software_coordinate_system.coordinate_system
    assert system == CartesianCoordinateSystem(
        coordinate_handedness=software_coordinate_system.coordinate_handedness,
        axis_orientation=software_coordinate_system.axis_orientation,
    )


@pytest.mark.parametrize("software_coordinate_system", IMPLEMENTED_SYSTEMS)
def test_orientation_is_consistent_with_handedness(
    software_coordinate_system: SoftwareCoordinateSystem,
) -> None:
    """`right x up` equals `forward` times the handedness sign (finger mnemonic)."""
    system: CartesianCoordinateSystem = software_coordinate_system.coordinate_system
    cross_product = np.cross(system.right.unit_vector, system.up.unit_vector)
    np.testing.assert_array_equal(
        cross_product,
        system.coordinate_handedness.cross_product_value * system.forward.unit_vector,
    )


@pytest.mark.parametrize(
    "software_coordinate_system",
    [
        SoftwareCoordinateSystem.UNREAL_ENGINE,
        SoftwareCoordinateSystem.UNITY,
        SoftwareCoordinateSystem.AUTOCAD,
    ],
)
def test_coordinate_handedness_not_implemented(
    software_coordinate_system: SoftwareCoordinateSystem,
) -> None:
    """Softwares without a defined handedness raise `NotImplementedError`."""
    with pytest.raises(NotImplementedError):
        _ = software_coordinate_system.coordinate_handedness


@pytest.mark.parametrize(
    "software_coordinate_system",
    [
        SoftwareCoordinateSystem.UNREAL_ENGINE,
        SoftwareCoordinateSystem.UNITY,
        SoftwareCoordinateSystem.AUTOCAD,
        SoftwareCoordinateSystem.BLENDER,
    ],
)
def test_axis_orientation_and_coordinate_system_not_implemented(
    software_coordinate_system: SoftwareCoordinateSystem,
) -> None:
    """Softwares without a defined orientation raise `NotImplementedError`."""
    with pytest.raises(NotImplementedError):
        _ = software_coordinate_system.axis_orientation
    with pytest.raises(NotImplementedError):
        _ = software_coordinate_system.coordinate_system
