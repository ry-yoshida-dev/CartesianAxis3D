"""Tests for `cartesian_axis.AxisName`."""

from __future__ import annotations

import pytest

from cartesian_axis import AxisName


@pytest.mark.parametrize(
    ("axis_name", "expected_other_axes"),
    [
        (AxisName.FORWARD, (AxisName.RIGHT, AxisName.UP)),
        (AxisName.RIGHT, (AxisName.FORWARD, AxisName.UP)),
        (AxisName.UP, (AxisName.FORWARD, AxisName.RIGHT)),
    ],
)
def test_other_axes_returns_remaining_axis_names(
    axis_name: AxisName,
    expected_other_axes: tuple[AxisName, AxisName],
) -> None:
    """`other_axes` returns the two remaining axis names in declaration order."""
    assert axis_name.other_axes == expected_other_axes


@pytest.mark.parametrize("axis_name", list(AxisName))
def test_other_axes_excludes_self(axis_name: AxisName) -> None:
    """`other_axes` never contains the axis name itself."""
    assert axis_name not in axis_name.other_axes
