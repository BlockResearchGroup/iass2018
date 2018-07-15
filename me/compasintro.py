import compas

from compas.datastructures import Mesh
from compas.plotters import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

mesh.update_default_vertex_attributes({
    'is_fixed': False,
    'weight'  : 1.0,
    'px'      : 0.0,
    'py'      : 0.0,
    'pz'      : 0.0
})

x = mesh.get_vertices_attribute('x', keys=mesh.vertices_where({'vertex_degree': 2}))

print(x)

# plotter = MeshPlotter(mesh, figsize=(10, 7))

# plotter.draw_vertices(
#     text={key: key for key in mesh.vertices()},
#     radius=0.2,
#     facecolor={key: (255, 0, 0) for key in mesh.vertices_where({'vertex_degree': 2})}
# )
# plotter.draw_edges()
# plotter.draw_faces()

# plotter.show()

