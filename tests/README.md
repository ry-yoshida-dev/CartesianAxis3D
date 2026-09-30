# tests

## Overview

Pytest suite for `cartesian_axis`. The package is installed editable
(`pip install -e .`), so tests import it through its public API only.

Run the full suite from the repository root:

```bash
.venv/bin/python -m pytest
```

Besides per-class behavior, the suite checks that every predefined
`SoftwareCoordinateSystem` is internally consistent: `right x up` must equal
`forward` multiplied by the handedness sign (the finger mnemonic documented on
`AxisOrientation`).

## Components

| Component | Description |
| --- | --- |
| [test_axis.py](./test_axis.py) | `Axis` index mapping, other axes, and unit vectors. |
| [test_axis_name.py](./test_axis_name.py) | `AxisName.other_axes`. |
| [test_axis_vectors.py](./test_axis_vectors.py) | `AxisVectors` construction, access, registration, and array round trips. |
| [test_handedness.py](./test_handedness.py) | `CoordinateHandedness` flags and cross-product sign. |
| [test_orientation.py](./test_orientation.py) | `AxisOrientation` validation, up-axis flags, unit vectors, and Plotly conversion indices. |
| [test_coordinate_system.py](./test_coordinate_system.py) | `CartesianCoordinateSystem` delegation, immutability, and equality. |
| [test_software_coordinate_system.py](./test_software_coordinate_system.py) | Predefined software conventions, handedness consistency, and unimplemented cases. |
| [test_package_init.py](./test_package_init.py) | Public API exposed through `__all__`. |
