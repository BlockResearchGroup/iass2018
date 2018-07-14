from __future__ import print_function

import compas
from compas.datastructures import Mesh
from compas.plotters import MeshPlotter


# ==============================================================================
# construct a mesh from OBJ

mesh = Mesh.from_obj(compas.get('faces.obj'))


# ==============================================================================
# visualise the result with a plotter

plotter = MeshPlotter(mesh, figsize=(10, 7))

plotter.draw_vertices(
    text={key: key for key in mesh.vertices_where({'x': (2, 8), 'y': (2, 8)})},
    radius={key: 0.2 for key in mesh.vertices_where({'x': (2, 8), 'y': (2, 8)})}
)
plotter.draw_edges()
plotter.draw_faces()

plotter.show()
