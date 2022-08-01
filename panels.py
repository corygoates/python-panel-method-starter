import numpy as np


class Panel:
    """A class defining a triangular panel for potential flow simulation."""

    def __init__(self, v0, v1, v2, i0, i1, i2):

        # Store vertices
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

        # Store vertex indices (necessary for VTK export)
        self.i0 = i0
        self.i1 = i1
        self.i2 = i2

        # Initialize neighbor list
        self.neighbors = []