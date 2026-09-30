"""Tests for `cartesian_axis.CoordinateHandedness`."""

from __future__ import annotations

import pytest

from cartesian_axis import CoordinateHandedness


@pytest.mark.parametrize(
    ("handedness", "is_right_handed", "is_left_handed"),
    [
        (CoordinateHandedness.RIGHT, True, False),
        (CoordinateHandedness.LEFT, False, True),
    ],
)
def test_handedness_flags(
    handedness: CoordinateHandedness,
    is_right_handed: bool,
    is_left_handed: bool,
) -> None:
    """Exactly one of the handedness flags is set."""
    assert handedness.is_right_handed is is_right_handed
    assert handedness.is_left_handed is is_left_handed


@pytest.mark.parametrize(
    ("handedness", "expected_sign"),
    [(CoordinateHandedness.RIGHT, 1), (CoordinateHandedness.LEFT, -1)],
)
def test_cross_product_value_sign(
    handedness: CoordinateHandedness,
    expected_sign: int,
) -> None:
    """`cross_product_value` is +1 for right-handed and -1 for left-handed."""
    assert handedness.cross_product_value == expected_sign
