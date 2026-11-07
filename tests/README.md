# tests

## Overview

Unit tests for the `cartesian_axis` package.

## Components

| Component | Description |
|-----------|-------------|
| [test_axis.py](./test_axis.py) | `Axis` index mapping, other axes, and unit vectors. |
| [test_axis_name.py](./test_axis_name.py) | `AxisName.other_axes`. |
| [test_axis_vector.py](./test_axis_vector.py) | Shape validation, copying, equality, and access of `AxisVectors`. |
| [test_axis_vectors.py](./test_axis_vectors.py) | `AxisVectors` construction, access, registration, and array round trips. |
| [test_handedness.py](./test_handedness.py) | `CoordinateHandedness` flags and cross-product sign. |
| [test_orientation.py](./test_orientation.py) | Validation, role lookup, and converting indices of `AxisOrientation`. |
| [test_coordinate_system.py](./test_coordinate_system.py) | `CartesianCoordinateSystem` delegation, immutability, and equality. |
| [test_software_coordinate_system.py](./test_software_coordinate_system.py) | Predefined software coordinate system conventions. |
| [test_package_init.py](./test_package_init.py) | Public API exposed through `__all__`. |
