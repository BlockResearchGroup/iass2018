import compas

from compas.datastructures import Mesh
from compas.plotters import MeshPlotter
from compas.utilities import i_to_rgb

from compas.numerical import mesh_fd_numpy


# ==============================================================================
# construct a mesh from OBJ

mesh = Mesh.from_obj(compas.get('faces.obj'))

mesh.update_default_vertex_attributes({'is_fixed': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
mesh.update_default_edge_attributes({'q': 1.0})


# for uv in mesh.edges_on_boundary():
#     mesh.set_edge_attribute(uv, 'q', 10)

# # ==============================================================================
# # update the boundary conditions

# for key, attr in mesh.vertices(True):
#     attr['is_fixed'] = mesh.vertex_degree(key) == 2


# # ==============================================================================
# # create a plotter for visualisation

# plotter = MeshPlotter(mesh, figsize=(10, 7))

# plotter.draw_as_lines(color='#cccccc', width=0.5)


# # ==============================================================================
# # apply force density

# mesh_fd_numpy(mesh)


# # ==============================================================================
# # visualise the result

# zmax = max(mesh.get_vertices_attribute('z'))
# fmax = max(mesh.get_edges_attribute('f'))

# plotter.draw_vertices()
# plotter.draw_faces()
# plotter.draw_edges(
#     width={(u, v): 10 * attr['f'] / fmax for u, v, attr in mesh.edges(True)},
#     color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in mesh.edges(True)},
# )

# plotter.show()
