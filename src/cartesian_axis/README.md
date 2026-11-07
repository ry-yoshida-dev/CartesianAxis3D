# cartesian_axis

## Overview

Utilities for 3D Cartesian coordinate systems: axis definitions, axis roles (forward / right / up), handedness, and predefined conventions of software tools.

A coordinate system is described by two independent parts:

- `AxisOrientation` assigns the forward, right, and up roles to the X, Y, and Z axes. The positive direction of each axis is not specified (e.g. OpenCV's up axis Y points downward).
- `CoordinateHandedness` tells which hand's thumb, index finger, and middle finger point along the positive X, Y, and Z axes.

## Components

| Component | Description |
|-----------|-------------|
| [axis.py](./axis.py) | Enum of the X, Y, and Z axes with index and unit vector helpers. |
| [axis_name.py](./axis_name.py) | Enum of the forward, right, and up roles. |
| [axis_vector.py](./axis_vector.py) | Container of per-axis vectors of shape (3,) with shape validation and value equality. |
| [orientation.py](./orientation.py) | Assignment of roles to axes and index permutation between orientations. |
| [handedness.py](./handedness.py) | Enum of right-handed and left-handed coordinates. |
| [coordinate_system.py](./coordinate_system.py) | Cartesian coordinate system combining handedness and axis orientation. |
| [software_coordinate_system.py](./software_coordinate_system.py) | Conventions of Blender, Unreal Engine, Unity, AutoCAD, Plotly, and OpenCV. |
| [py.typed](./py.typed) | PEP 561 marker for type checkers. |

## Examples

```python
import numpy as np

from cartesian_axis import (
    Axis,
    AxisOrientation,
    CartesianCoordinateSystem,
    CoordinateHandedness,
    SoftwareCoordinateSystem,
)

system = CartesianCoordinateSystem(
    coordinate_handedness=CoordinateHandedness.RIGHT,
    axis_orientation=AxisOrientation(forward=Axis.Z, right=Axis.X, up=Axis.Y),
)

indices = system.get_converting_indices(
    software_coordinate_system=SoftwareCoordinateSystem.PLOTLY
)
points = np.array([[1.0, 2.0, 3.0]])
points_for_plotly = points[:, indices]
```
