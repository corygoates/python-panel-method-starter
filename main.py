import sys
import json

import numpy as np
import pyvista as pv

from panels import Panel
from vkt import load_vtk

if __name__=="__main__":

    # Get input file
    input_file = sys.argv[-1]
    with open(input_file) as input_handle:
        input_vals = json.load(input_handle)

    # Load geometry
    geometry_file = input_vals["geometry"]["file"]
    N, panels, vertices = load_vtk(geometry_file)






    # Here's where the magic happens....





    # Write output
    output_file = input_vals["output"]["file"]
    export_vtk(output_file, panels, vertices)