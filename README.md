# CartesianAxis3D

## Overview

`cartesian_axis` is a Python package for **3D Cartesian coordinate systems**: axis enums, **handedness**, **axis orientation** (forward / right / up mapped to X, Y, Z), `CartesianCoordinateSystem`, and predefined conventions of software tools.

See [src/cartesian_axis/README.md](src/cartesian_axis/README.md) for package details.

## Installation

From the project root:

```bash
pip install -e ".[dev]"
```

## Usage

```python
from cartesian_axis import SoftwareCoordinateSystem

opencv_system = SoftwareCoordinateSystem.OPENCV.coordinate_system
indices = opencv_system.get_converting_indices(
    software_coordinate_system=SoftwareCoordinateSystem.PLOTLY
)
```

## Development

```bash
pytest
mypy src tests
ruff check src tests
```
