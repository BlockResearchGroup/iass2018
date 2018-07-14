import compas
from compas.datastructures import Mesh
from compas.plotters import MeshPlotter


mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices(
    text={key: key for key in mesh.vertices_where({'x': (2, 8), 'y': (2, 8)})},
    radius={key: 0.2 for key in mesh.vertices_where({'x': (2, 8), 'y': (2, 8)})}
)
plotter.draw_edges()
plotter.draw_faces()

plotter.show()