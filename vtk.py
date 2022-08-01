import numpy as np
import pyvista as pv

from panels import Panel


def load_vtk(filename):
    """Loads a surface mesh from the specified VTK file.
    
    Parameters
    ----------
    filename : string
        File to load vtk from.

    Returns
    -------
    N : integer
        Number of panels.

    panels : list
        List of panel objects.
    """

    # Get mesh data
    mesh_data = pv.read(vtk_file)

    # Get vertices
    vertices = np.copy(mesh_data.points)

    # Initialize panels
    panels = []
    N = mesh_data.n_faces
    panel_vertex_indices = []
    curr_ind = 0
    cell_info = mesh_data.faces
    for i in range(self.N):

        # Determine number of edges and vertex indices
        n = cell_info[curr_ind]
        vertex_ind = cell_info[curr_ind+1:curr_ind+1+n]
        panel_vertex_indices.append([n, *list(vertex_ind)])
        vertices = vertices[vertex_ind]

        # Initialize panel object
        panel_obj = Panel(vertices[0], vertices[1], vertices[2], vertex_ind[0], vertex_ind[1], vertex_ind[2])

        # Store
        panels.append(panel_obj)

        # Update index
        curr_ind += n+1

    # Determine panel neighbors
    for i, panel_i in enumerate(panels):

        # loop through possible neighbors
        for j, panel_j in enumerate(panels[i+1:]):

            # Determine if we're touching and/or abutting
            num_shared = 0
            for i_vert in panel_vertex_indices[i][1:]:

                # Check for shared vertex
                if i_vert in panel_vertex_indices[j][1:]:
                    num_shared += 1
                    if num_shared==2:
                        break # Don't need to keep going
                    
            # Abutting panels (two shared vertices)
            if num_shared==2 and j not in panel_i.neighbors:
                panel_i.neighbors.append(j)
                panel_j.neighbors.append(i)

    return N, panel, vertices


    def export_vtk(filename, panels, vertices, results=[]):
        """Exports the mesh and computation results to a VTK file.

        Parameters
        ----------
        filename : str
            Name of the file to write the results to. Must have '.vtk' extension.

        panels : list
            List of panel objects.

        vertices : ndarray
            Array of vertex locations.

        results : list, optional
            Optional cell-based outputs. Each element of this list should have the structure

            {
                "name" : <NAME OF OUTPUT VARIABLE>,
                "type" : "scalar", "vector", or "normal",
                "value" : <ARRAY OF OUTPUT VALUES>
            }
        """

        # Check extension
        if '.vtk' not in filename:
            raise IOError("Filename for VTK export must contain .vtk extension.")

        # Open file
        with open(filename, 'w') as export_handle:
            
            # Write header
            print("# vtk DataFile Version 3.0", file=export_handle)
            print("Panel method results file. Generated by python-panel-method-starter, Cory Goates (c) 2022.", file=export_handle)
            print("ASCII", file=export_handle)

            # Write dataset
            print("DATASET POLYDATA", file=export_handle)

            # Write vertices
            print("POINTS {0} float".format(len(vertices)), file=export_handle)
            for vertex in vertices:
                print("{0:<20.12}{1:<20.12}{2:<20.12}".format(*vertex), file=export_handle)

            # Determine polygon list size
            size = 4*len(panels)

            # Write panels
            print("POLYGONS {0} {1}".format(len(panels), size), file=export_handle)
            for panel in panels:
                print("3 {0} {1} {2}".format(panel.i0, panel.i1, panel.i2)), file=export_handle)

            # Write panel data
            print("CELL_DATA {0}".format(len(panels)), file=export_handle)

            # Write results
            for result in results:

                # Get type
                result_type = result["type"]

                # Write scalars
                if result_type == "scalar":

                    print("SCALARS {0} float 1".format(result["name"]), file=export_handle)
                    print("LOOKUP_TABLE default", file=export_handle)
                    for val in result["value"]:
                        print("{0:<20.12}".format(val), file=export_handle)

                # Write vectors
                print("VECTORS {0} float".format(result["name"]), file=export_handle)
                for val in result["value"]:
                    print("{0:<20.12} {1:<20.12} {2:<20.12}".format(val[0], val[1], val[2]), file=export_handle)

                # Write normals
                print("NORMALS {0} float".format(result["name"]), file=export_handle)
                for val in result["value"]:
                    print("{0:<20.12} {1:<20.12} {2:<20.12}".format(val[0], val[1], val[2]), file=export_handle)