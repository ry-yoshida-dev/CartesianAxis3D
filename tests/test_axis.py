"""Tests for `cartesian_axis.Axis`."""

from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from cartesian_axis import Axis


@pytest.mark.parametrize(
    ("axis", "expected_other_axes"),
    [
        (Axis.X, (Axis.Y, Axis.Z)),
        (Axis.Y, (Axis.X, Axis.Z)),
        (Axis.Z, (Axis.X, Axis.Y)),
    ],
)
def test_other_axes_returns_remaining_axes_in_order(
    axis: Axis,
    expected_other_axes: tuple[Axis, Axis],
) -> None:
    """`other_axes` returns the two remaining axes in X/Y/Z order."""
    assert axis.other_axes == expected_other_axes


@pytest.mark.parametrize(
    ("axis", "expected_index"),
    [(Axis.X, 0), (Axis.Y, 1), (Axis.Z, 2)],
)
def test_to_index_returns_array_position(axis: Axis, expected_index: int) -> None:
    """`to_index` maps each axis to its position in an XYZ array."""
    assert axis.to_index == expected_index


@pytest.mark.parametrize("axis", list(Axis))
def test_from_index_round_trips_with_to_index(axis: Axis) -> None:
    """`from_index` is the inverse of `to_index`."""
    assert Axis.from_index(axis.to_index) is axis


@pytest.mark.parametrize("invalid_index", [-1, 3, 100])
def test_from_index_rejects_out_of_range_index(invalid_index: int) -> None:
    """`from_index` raises `ValueError` for indices outside 0..2."""
    with pytest.raises(ValueError, match="Invalid index"):
        _ = Axis.from_index(invalid_index)


@pytest.mark.parametrize(
    ("axis", "expected_unit_vector"),
    [
        (Axis.X, [1.0, 0.0, 0.0]),
        (Axis.Y, [0.0, 1.0, 0.0]),
        (Axis.Z, [0.0, 0.0, 1.0]),
    ],
)
def test_unit_vector_points_along_axis(
    axis: Axis,
    expected_unit_vector: list[float],
) -> None:
    """`unit_vector` is the standard basis vector of the axis."""
    np.testing.assert_array_equal(axis.unit_vector, np.array(expected_unit_vector))


@pytest.mark.parametrize("axis", list(Axis))
def test_unit_vector_matches_identity_row(axis: Axis) -> None:
    """`unit_vector` equals the identity-matrix row at `to_index`."""
    identity: NDArray[np.float64] = np.eye(3)
    np.testing.assert_array_equal(axis.unit_vector, identity[axis.to_index, :])


@pytest.mark.parametrize("axis", list(Axis))
def test_unit_vector_is_float64(axis: Axis) -> None:
    """`unit_vector` has the float64 dtype declared in its annotation."""
    assert axis.unit_vector.dtype == np.float64
