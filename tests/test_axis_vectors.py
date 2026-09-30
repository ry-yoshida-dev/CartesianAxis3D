"""Tests for `cartesian_axis.AxisVectors`."""

from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import NDArray

from cartesian_axis import Axis, AxisVectors

SAMPLE_ROWS: dict[Axis, NDArray[np.float64]] = {
    Axis.X: np.array([0.0, 1.0, 2.0]),
    Axis.Y: np.array([3.0, 4.0, 5.0]),
    Axis.Z: np.array([6.0, 7.0, 8.0]),
}


@pytest.fixture
def sample_array() -> NDArray[np.float64]:
    """A 3x3 array whose rows are distinguishable per axis."""
    return np.stack([SAMPLE_ROWS[Axis.X], SAMPLE_ROWS[Axis.Y], SAMPLE_ROWS[Axis.Z]])


def test_zero_vectors_are_all_zero() -> None:
    """`zero_vectors` creates three zero vectors of length 3."""
    axis_vectors: AxisVectors = AxisVectors.zero_vectors()
    np.testing.assert_array_equal(axis_vectors.to_array(), np.zeros((3, 3)))


def test_zero_vectors_do_not_share_memory() -> None:
    """Each zero vector is an independent array."""
    axis_vectors: AxisVectors = AxisVectors.zero_vectors()
    axis_vectors.x[0] = 1.0
    assert axis_vectors.y[0] == 0.0
    assert axis_vectors.z[0] == 0.0


def test_from_array_assigns_rows_in_xyz_order(
    sample_array: NDArray[np.float64],
) -> None:
    """`from_array` assigns rows 0, 1, 2 to x, y, z."""
    axis_vectors: AxisVectors = AxisVectors.from_array(sample_array)
    np.testing.assert_array_equal(axis_vectors.x, SAMPLE_ROWS[Axis.X])
    np.testing.assert_array_equal(axis_vectors.y, SAMPLE_ROWS[Axis.Y])
    np.testing.assert_array_equal(axis_vectors.z, SAMPLE_ROWS[Axis.Z])


def test_to_array_round_trips_with_from_array(
    sample_array: NDArray[np.float64],
) -> None:
    """`to_array` restores the array passed to `from_array`."""
    axis_vectors: AxisVectors = AxisVectors.from_array(sample_array)
    np.testing.assert_array_equal(axis_vectors.to_array(), sample_array)


@pytest.mark.parametrize("invalid_shape", [(3,), (2, 3), (3, 4), (3, 3, 1)])
def test_from_array_rejects_non_3x3_array(invalid_shape: tuple[int, ...]) -> None:
    """`from_array` raises `ValueError` unless the array is 3x3."""
    with pytest.raises(ValueError, match=r"shape \(3, 3\)"):
        _ = AxisVectors.from_array(np.zeros(invalid_shape))


@pytest.mark.parametrize("axis", list(Axis))
def test_get_returns_vector_for_axis(
    axis: Axis,
    sample_array: NDArray[np.float64],
) -> None:
    """`get` returns the row matching the axis index."""
    axis_vectors: AxisVectors = AxisVectors.from_array(sample_array)
    np.testing.assert_array_equal(axis_vectors.get(axis), SAMPLE_ROWS[axis])


@pytest.mark.parametrize("axis", list(Axis))
def test_register_replaces_only_target_axis(axis: Axis) -> None:
    """`register` overwrites the target axis and leaves the others untouched."""
    axis_vectors: AxisVectors = AxisVectors.zero_vectors()
    vector: NDArray[np.float64] = np.array([1.0, 2.0, 3.0])

    axis_vectors.register(axis, vector)

    np.testing.assert_array_equal(axis_vectors.get(axis), vector)
    for other_axis in axis.other_axes:
        np.testing.assert_array_equal(axis_vectors.get(other_axis), np.zeros(3))
