# import sys
# import os

# sys.path.insert(0, '/Users/vanmelet/Code/compas-dev/compas/src')

import compas
import compas_rhino

from compas.datastructures import Mesh

from compas_rhino import MeshArtist
from compas_rhino import mesh_from_surface_uv


# ==============================================================================
# construct a mesh from a surface UV space

guid = compas_rhino.select_surface()
mesh = mesh_from_surface_uv(Mesh, guid)


# ==============================================================================
# visualise the result

artist = MeshArtist(mesh)

artist.draw_vertices()
artist.draw_edges()
artist.draw_faces()

artist.redraw()
