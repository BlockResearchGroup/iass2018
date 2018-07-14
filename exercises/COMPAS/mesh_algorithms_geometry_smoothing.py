import compas

from compas.datastructures import Mesh
from compas.plotters import MeshPlotter
from compas.geometry import smooth_centroid


# ==============================================================================
# construct a mesh from OBJ

mesh = Mesh.from_obj(compas.get('faces.obj'))


# ==============================================================================
# update the boundary conditions

vertices  = mesh.get_vertices_attributes('xyz')
faces     = [mesh.face_vertices(fkey) for fkey in mesh.faces()]
adjacency = [mesh.vertex_neighbours(key) for key in mesh.vertices()]
fixed     = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]


# ==============================================================================
# store the original geometry

lines = []
for u, v in mesh.edges():
    lines.append({
        'start': mesh.vertex_coordinates(u, 'xy'),
        'end'  : mesh.vertex_coordinates(v, 'xy'),
        'color': '#cccccc',
        'width': 1.0,
    })


# ==============================================================================
# smooth

smooth_centroid(vertices, adjacency, fixed=fixed, kmax=100)

for key, attr in mesh.vertices(True):
    attr['x'] = vertices[key][0]
    attr['y'] = vertices[key][1]
    attr['z'] = vertices[key][2]


# ==============================================================================
# visualise the result

plotter = MeshPlotter(mesh, figsize=(10, 7))

plotter.draw_lines(lines)
plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
plotter.draw_edges()

plotter.show()

