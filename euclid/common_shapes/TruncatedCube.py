from numpy import sqrt
import numpy
from euclid.polyhedron import ConvexPolyhedron

# Example:
# from euclid.polyhedron.TruncatedCube import shape
points = [
    (-1 / 2, 1 / 2 + 1 / sqrt(2), 1 / 2 + 1 / sqrt(2)),
    (-1 / 2, 1 / 2 + 1 / sqrt(2), (2 - 2 * sqrt(2))**(-1)),
    (-1 / 2, (2 - 2 * sqrt(2))**(-1), 1 / 2 + 1 / sqrt(2)),
    (-1 / 2, (2 - 2 * sqrt(2))**(-1), (2 - 2 * sqrt(2))**(-1)),
    (1 / 2, 1 / 2 + 1 / sqrt(2), 1 / 2 + 1 / sqrt(2)),
    (1 / 2, 1 / 2 + 1 / sqrt(2), (2 - 2 * sqrt(2))**(-1)),
    (1 / 2, (2 - 2 * sqrt(2))**(-1), 1 / 2 + 1 / sqrt(2)),
    (1 / 2, (2 - 2 * sqrt(2))**(-1), (2 - 2 * sqrt(2))**(-1)),
    (1 / 2 + 1 / sqrt(2), -1 / 2, 1 / 2 + 1 / sqrt(2)),
    (1 / 2 + 1 / sqrt(2), -1 / 2, (2 - 2 * sqrt(2))**(-1)),
    (1 / 2 + 1 / sqrt(2), 1 / 2, 1 / 2 + 1 / sqrt(2)),
    (1 / 2 + 1 / sqrt(2), 1 / 2, (2 - 2 * sqrt(2))**(-1)),
    (1 / 2 + 1 / sqrt(2), 1 / 2 + 1 / sqrt(2), -1 / 2),
    (1 / 2 + 1 / sqrt(2), 1 / 2 + 1 / sqrt(2), 1 / 2),
    (1 / 2 + 1 / sqrt(2), (2 - 2 * sqrt(2))**(-1), -1 / 2),
    (1 / 2 + 1 / sqrt(2), (2 - 2 * sqrt(2))**(-1), 1 / 2),
    ((2 - 2 * sqrt(2))**(-1), -1 / 2, 1 / 2 + 1 / sqrt(2)),
    ((2 - 2 * sqrt(2))**(-1), -1 / 2, (2 - 2 * sqrt(2))**(-1)),
    ((2 - 2 * sqrt(2))**(-1), 1 / 2, 1 / 2 + 1 / sqrt(2)),
    ((2 - 2 * sqrt(2))**(-1), 1 / 2, (2 - 2 * sqrt(2))**(-1)),
    ((2 - 2 * sqrt(2))**(-1), 1 / 2 + 1 / sqrt(2), -1 / 2),
    ((2 - 2 * sqrt(2))**(-1), 1 / 2 + 1 / sqrt(2), 1 / 2),
    ((2 - 2 * sqrt(2))**(-1), (2 - 2 * sqrt(2))**(-1), -1 / 2),
    ((2 - 2 * sqrt(2))**(-1), (2 - 2 * sqrt(2))**(-1), 1 / 2),
]

shape = ConvexPolyhedron(numpy.array(points))
