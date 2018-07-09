from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas_rhino.utilities import XFunc
from compas_rhino.utilities import get_meshes
from compas_rhino.utilities import get_points
from compas_rhino.utilities import get_point_coordinates
from compas_rhino.utilities import get_lines
from compas_rhino.utilities import get_line_coordinates

from compas_rhino.helpers import mesh_from_guid

from compas.utilities import pairwise
from compas.utilities import geometric_key

from compas_tna.rhino import RhinoFormDiagram
from compas_tna.rhino import RhinoForceDiagram

horizontal = XFunc('compas_tna.equilibrium.horizontal')
vertical_from_zmax = XFunc('compas_tna.equilibrium.vertical_from_zmax')


__author__    = ['Tom Van Mele', 'Tomas Mendez Echenagucia']
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


# get rhino mesh guid from layer -----------------------------------------------
guid = get_meshes(layer='mesh')[0]

# make rhino form diagram ------------------------------------------------------
form = mesh_from_guid(RhinoFormDiagram, guid)

# set anchor points ------------------------------------------------------------
for key in form.vertices_where({'vertex_degree': 2}):
    form.vertex[key]['is_anchor'] = True

guids = get_points('pts')
pts = get_point_coordinates(guids)
gk_dict = form.gkey_key()
gks= [gk_dict[geometric_key(pt)] for pt in pts]

for key in gks:
    form.vertex[key]['is_anchor'] = True

# find open faces (conv. function to come) -------------------------------------
boundary = form.vertices_on_boundary(ordered=True)

unsupported = [[]]
for key in boundary:
    unsupported[-1].append(key)
    if form.vertex[key]['is_anchor']:
        unsupported.append([key])

unsupported[-1] += unsupported[0]
del unsupported[0]

for vertices in unsupported:
    fkey = form.add_face(vertices, is_unloaded=True)

# set non-edges (conv. function to come) ---------------------------------------
for vertices in unsupported:
    u = vertices[-1]
    v = vertices[0]
    form.set_edge_attribute((u, v), 'is_edge', False)

# make rhino force diagram -----------------------------------------------------
force = RhinoForceDiagram.from_formdiagram(form)

# set fmins - fmaxs ------------------------------------------------------------
fmin = 3
fmax = 5
guids = get_lines(layer='edges')
lines = get_line_coordinates(guids)
edges = [[gk_dict[geometric_key(u)], gk_dict[geometric_key(v)]] for u, v in lines]

for u, v in edges:
    u_ = form.halfedge[u][v]
    v_ = form.halfedge[v][u]
    force.set_edge_attribute((u_, v), 'lmin', fmin)
    force.set_edge_attribute((u_, v), 'lmax', fmax)

# horizontal equilibrium -------------------------------------------------------
formdata, forcedata = horizontal(form.to_data(), force.to_data(), kmax=1000)

# vertical equilibrium ---------------------------------------------------------
formdata, forcedata = vertical_from_zmax(formdata, forcedata, zmax=3, display=False)
form.data = formdata
force.data = forcedata

# rhino drawing ----------------------------------------------------------------
form.draw()
force.draw()
