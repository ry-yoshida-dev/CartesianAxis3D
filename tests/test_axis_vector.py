import numpy as np
import pytest
from numpy.typing import NDArray

from cartesian_axis import Axis, AxisVectors


class TestAxisVectors:
    """Tests for AxisVectors."""

    def test_from_array_copies_input(self) -> None:
        array: NDArray[np.float64] = np.eye(3)
        axis_vectors: AxisVectors = AxisVectors.from_array(array)
        array[0, 0] = 5.0
        np.testing.assert_array_equal(axis_vectors.get(Axis.X), [1.0, 0.0, 0.0])

    def test_invalid_shape_raises(self) -> None:
        with pytest.raises(ValueError, match="shape"):
            AxisVectors.from_array(np.zeros((2, 3)))
        with pytest.raises(ValueError, match="shape"):
            AxisVectors.zero_vectors().register(Axis.Y, [1.0, 2.0])

    def test_register_and_to_array(self) -> None:
        axis_vectors: AxisVectors = AxisVectors.zero_vectors()
        axis_vectors.register(Axis.Z, [1, 2, 3])
        assert axis_vectors.get(Axis.Z).dtype == np.float64
        np.testing.assert_array_equal(axis_vectors.to_array()[2], [1.0, 2.0, 3.0])

    def test_equality_compares_values(self) -> None:
        assert AxisVectors.from_array(np.eye(3)) == AxisVectors.from_array(np.eye(3))
        assert AxisVectors.from_array(np.eye(3)) != AxisVectors.zero_vectors()
        assert AxisVectors.zero_vectors() != "zero"
