# CartesianAxis3D

## Overview

`cartesian_axis` is a Python package for **3D Cartesian coordinate systems**: axis enums, **handedness**, **axis orientation** (forward / right / up mapped to X, Y, Z), `CartesianCoordinateSystem`.

See [src/cartesian_axis/README.md](src/cartesian_axis/README.md) for package details.

## Installation

From the project root:

```bash
pip install -e .
```

## Usage

```python
from cartesian_axis import (
    Axis,
    AxisOrientation,
    CartesianCoordinateSystem,
    CoordinateHandedness,
    SoftwareCoordinateSystem,
)

orientation = AxisOrientation(forward=Axis.X, right=Axis.Y, up=Axis.Z)
system = CartesianCoordinateSystem(
    coordinate_handedness=CoordinateHandedness.RIGHT,
    axis_orientation=orientation,
)
```

## Testing

```bash
pip install -e . pytest
python -m pytest
```

See [tests/README.md](tests/README.md) for what the suite covers.
