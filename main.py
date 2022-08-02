import sys
import json

import numpy as np

from vtk import load_vtk, export_vtk

if __name__=="__main__":

    # Get input file
    input_file = sys.argv[-1]
    with open(input_file) as input_handle:
        input_vals = json.load(input_handle)

    # Load geometry
    geometry_file = input_vals["geometry"]["file"]
    N_panels, N_verts, panels, vertices = load_vtk(geometry_file)
    print("Read in {0} panels and {1} vertices from {2}.".format(N_panels, N_verts, geometry_file))






    # Here's where the magic happens....





    # Write output
    output_file = input_vals["output"]["file"]
    example_result = {
        "name" : "example_result",
        "type" : "scalar",
        "value" : np.linspace(1, 2, N_panels)
    }
    export_vtk(output_file, panels, vertices, results=[example_result])
    print("Wrote results to {0}.".format(output_file))