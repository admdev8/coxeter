from abc import abstractmethod
from .shape_family import _ShapeFamily
from ..shape_classes import ConvexPolyhedron
import numpy as np
from scipy.constants import golden_ratio


class TruncationPlaneShapeFamily(_ShapeFamily):
    """A family of shapes that can be constructed based on the intersection of
    a set of half spaces defined by a symmetric set of planes.

    This family of shapes is defined in :cite:`Chen2014`. A set of planes are
    symmetrically placed about a central point, and shapes are defined by the
    intersection of the half spaces defined by these planes. Depending on the
    symmetry group chosen to define the planes, different shapes can result.
    Subclasses of this class must define the :attr:`~.planes` and
    :attr:`~.plane_types` properties to define the planes and which distance
    parameter is used to define those truncations.

    The following parameters are required by this class:

      - :math:`a`
      - :math:`b`
      - :math:`c`

    See :cite:`Chen2014` for descriptions of these parameters. The bounds of
    each parameter are set by the subclasses.
    """
    def make_vertices(self, a, b, c):
        """Generate vertices from the a, b, and c parameters.

        Args:
            a (float): The a parameter.
            b (float): The b parameter.
            c (float): The c parameter.

        Returns:
            (:math:`N_{vertices}`, 3) :class:`numpy.ndarray` of float:
                The vertices of the shape generated by the provided parameters.
        """
        # Vectorize the plane distances.
        dists = np.array([a, b, c])

        thresh = 1e-6

        planetypes = self.plane_types
        planelist = self.planes

        num_planes = len(planetypes)
        indices = [(i, j, k) for i in range(num_planes) for j in
                   range(i+1, num_planes) for k in range(j+1, num_planes)]

        # Set up and solve a system of equations for the planes that should be
        # included.
        As = planelist[indices]
        alltypes = planetypes[indices]
        bs = dists[alltypes]

        dets = np.linalg.det(As)
        solution_indices = np.abs(dets) > thresh
        xs = np.linalg.solve(As[solution_indices], bs[solution_indices])

        # Get for each x whether any of the planes fail.
        dots = np.einsum('ik,jk', xs, planelist, optimize=True)
        alldists = dists[planetypes]
        dist_filter = (dots <= alldists[np.newaxis, :] + thresh).all(axis=1)
        passed_plane_test = xs[dist_filter]

        # We don't want to lose precision in the vertices to ensure that the
        # convex hull ends up finding the right faces, so get the unique
        # indices based on rounding but then use the original vertices.
        _, verts_indices = np.unique(
            passed_plane_test.round(6), axis=0, return_index=True)
        verts = passed_plane_test[verts_indices]

        return verts

    @property
    @abstractmethod
    def planes(self):
        """(:math:`N_{planes}`, 3) :class:`numpy.ndarray` of float: The set of
        defining planes"""
        pass

    @property
    @abstractmethod
    def plane_types(self):
        """(:math:`N_{planes}`, ) :class:`numpy.ndarray` of int: The types of
        the planes (type 0 corresponds to the parameter a, type 1 corresponds
        to b, and type 2 corresponds to c)."""
        pass


class Family323Plus(TruncationPlaneShapeFamily):
    R"""The 323+ shape family defined in :cite:`Chen2014`.

    The following parameters are required by this class:

      - :math:`a \in [1, 3]`
      - :math:`c \in [1, 3]`

    The :math:`b` parameter is always equal to 1 for this family.
    """

    def __call__(self, a, c):
        if not 1 <= a <= 3:
            raise ValueError("The a parameter must be between 1 and 3.")
        if not 1 <= c <= 3:
            raise ValueError("The c parameter must be between 1 and 3.")
        return ConvexPolyhedron(self.make_vertices(a, 1, c))

    @property
    def planes(self):
        return np.array([
            [1.0, 1.0, 1.0],
            [-1.0, -1.0, 1.0],
            [-1.0, 1.0, -1.0],
            [1.0, -1.0, -1.0],
            [1.0, 1.0, -1.0],
            [-1.0, -1.0, -1.0],
            [-1.0, 1.0, 1.0],
            [1.0, -1.0, 1.0],
            [1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0]])

    @property
    def plane_types(self):
        return np.array([2, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])


class Family423(TruncationPlaneShapeFamily):
    R"""The 423 shape family defined in :cite:`Chen2014`.

    The following parameters are required by this class:

      - :math:`a \in [1, 2]`
      - :math:`c \in [2, 3]`

    The :math:`b` parameter is always equal to 2 for this family.
    """

    def __call__(self, a, c):
        if not 1 <= a <= 2:
            raise ValueError("The a parameter must be between 1 and 2.")
        if not 2 <= c <= 3:
            raise ValueError("The c parameter must be between 2 and 3.")
        return ConvexPolyhedron(self.make_vertices(a, 2, c))

    @property
    def planes(self):
        return np.array([
             [1.0, 1.0, 1.0],
             [-1.0, -1.0, 1.0],
             [-1.0, 1.0, -1.0],
             [1.0, -1.0, -1.0],
             [1.0, 1.0, -1.0],
             [-1.0, -1.0, -1.0],
             [-1.0, 1.0, 1.0],
             [1.0, -1.0, 1.0],
             [1.0, 1.0, 0.0],
             [1.0, -1.0, 0.0],
             [-1.0, -1.0, 0.0],
             [-1.0, 1.0, 0.0],
             [1.0, 0.0, 1.0],
             [1.0, 0.0, -1.0],
             [-1.0, 0.0, -1.0],
             [-1.0, 0.0, 1.0],
             [0.0, 1.0, 1.0],
             [0.0, 1.0, -1.0],
             [0.0, -1.0, -1.0],
             [0.0, -1.0, 1.0],
             [1.0, 0.0, 0.0],
             [-1.0, 0.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, -1.0, 0.0],
             [0.0,  0.0,  1.0],
             [0.0, 0.0, -1.0]])

    @property
    def plane_types(self):
        return np.array([2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                         1, 1, 0, 0, 0, 0, 0, 0])


class Family523(TruncationPlaneShapeFamily):
    R"""The 423 shape family defined in :cite:`Chen2014`.

    The following parameters are required by this class:

      - :math:`a \in [1, s\sqrt{5}]`
      - :math:`c \in [S^2, 3]`

    where :math:`s = \frac{1}{2}\left(\sqrt{5} - 1\right)` and
    :math:`S = \frac{1}{2}\left(\sqrt{5} + 1\right)`.
    The :math:`b` parameter is always equal to 2 for this family.
    """

    """The constant s (the inverse of the golden ratio)."""
    s = 1 / golden_ratio

    """The constant S (the golden ratio)."""
    S = golden_ratio

    def __call__(self, a, c):
        if not 1 <= a <= (self.s*np.sqrt(5)):
            raise ValueError("The a parameter must be between 1 and s\u221A5 "
                             "(where s is the inverse of the golden ratio).")
        if not self.S**2 <= c <= 3:
            raise ValueError("The c parameter must be between S^2 and 3 "
                             "(where S is the golden ratio).")
        return ConvexPolyhedron(self.make_vertices(a, 2, c))

    @property
    def planes(self):
        s = self.s
        S = self.S
        return np.array([
            [1.0, 0.0, s],
            [-1.0, 0.0, -s],
            [-1.0, 0.0, s],
            [1.0, 0.0, -s],
            [0.0, -s, -1.0],
            [0.0, s, 1.0],
            [0.0, s, -1.0],
            [0.0, -s, 1.0],
            [-s, -1.0, 0.0],
            [s, 1.0, 0.0],
            [s, -1.0, 0.0],
            [-s, 1.0, 0.0],
            [-2.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [0.0, -2.0, 0.0],
            [0.0, 2.0, 0.0],
            [0.0, 0.0, -2.0],
            [0.0, 0.0, 2.0],
            [S, S, S],
            [-S, S, S],
            [S, -S, S],
            [S, S, -S],
            [S, -S, -S],
            [-S, -S, S],
            [-S, S, -S],
            [-S, -S, -S],
            [1.0, 0.0, S**2],
            [-1.0, 0.0, -S**2],
            [-1.0, 0.0, S**2],
            [1.0, 0.0, -S**2],
            [0.0, -S**2, -1.0],
            [0.0, S**2, 1.0],
            [0.0, -S**2, 1.0],
            [0.0, S**2, -1.0],
            [-S**2, -1.0, 0.0],
            [S**2, 1.0, 0.0],
            [S**2, -1.0, 0.0],
            [-S**2, 1.0, 0.0],
            [S, -1.0, -s],
            [-S, 1.0, -s],
            [-S, -1.0, s],
            [S, 1.0, s],
            [S, -1.0, s],
            [S, 1.0, -s],
            [-S, 1.0, s],
            [-S, -1.0, -s],
            [s, S, 1.0],
            [s, -S, -1.0],
            [-s, -S, 1.0],
            [-s, S, -1.0],
            [-s, -S, -1.0],
            [s, -S, 1.0],
            [-s, S, 1.0],
            [s, S, -1.0],
            [1.0, -s, -S],
            [-1.0, s, -S],
            [-1.0, -s, S],
            [1.0, s, S],
            [1.0, s, -S],
            [-1.0, s, S],
            [1.0, -s, S],
            [-1.0, -s, -S]
            ])

    @property
    def plane_types(self):
        return np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                         1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                         2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])


class TruncatedTetrahedronFamily(Family323Plus):
    R"""The truncated tetrahedron family used in :cite:`Damasceno2012`.

    The following parameters are required by this class:

      - truncation :math:`\in [0, 1]`

    This family is constructed as a limiting case of :class:`~.Family323Plus`
    with a = 1. The c value is then directly related to a linear interpolation
    over truncations. In particular, :math:`c = 3 - 2(\text{truncation})`.
    """

    def __call__(self, truncation):
        if not 0 <= truncation <= 1:
            raise ValueError("The truncation must be between 0 and 1.")
        c = 3 - 2 * truncation
        return super().__call__(1, c)
