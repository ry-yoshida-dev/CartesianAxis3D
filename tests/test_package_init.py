"""Tests for the public API exposed by `cartesian_axis`."""

from __future__ import annotations

import cartesian_axis


def test_all_lists_public_api() -> None:
    """`__all__` lists exactly the intended public names."""
    assert set(cartesian_axis.__all__) == {
        "Axis",
        "AxisVectors",
        "AxisName",
        "AxisOrientation",
        "CoordinateHandedness",
        "CartesianCoordinateSystem",
        "SoftwareCoordinateSystem",
    }


def test_all_names_are_importable() -> None:
    """Every name in `__all__` resolves to an attribute of the package."""
    for name in cartesian_axis.__all__:
        assert hasattr(cartesian_axis, name)
