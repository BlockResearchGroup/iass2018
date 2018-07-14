from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

from compas.utilities import XFunc

from compas_rhino.utilities import get_meshes
from compas_rhino.helpers import mesh_from_guid
from compas_rhino.utilities import get_points
from compas_rhino.utilities import get_point_coordinates

from compas.utilities import pairwise
from compas.utilities import geometric_key

from compas_tna.diagrams import FormDiagram
from compas_tna.diagrams import ForceDiagram

from compas_tna.rhino import FormArtist
from compas_tna.rhino import ForceArtist

__author__    = ['Tom Van Mele', 'Tomas Mendez Echenagucia']
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


def horizontal(form, force, *args, **kwargs):
    def callback(line, args):
        print(line)
        compas_rhino.wait()

    f = XFunc('compas_tna.equilibrium.horizontal_xfunc', callback=callback)
    formdata, forcedata = f(form.to_data(), force.to_data(), *args, **kwargs)
    form.data = formdata
    force.data = forcedata


def vertical_from_formforce_xfunc(form, force, *args, **kwargs):
    def callback(line, args):
        print(line)
        compas_rhino.wait()

    f = XFunc('compas_tna.equilibrium.vertical_from_formforce_xfunc', callback=callback)
    formdata, forcedata = f(form.to_data(), force.to_data(), *args, **kwargs)
    form.data = formdata
    force.data = forcedata


# get rhino mesh guid from layer -----------------------------------------------
guid = get_meshes(layer='mesh')[0]

# make rhino form diagram ------------------------------------------------------
form = mesh_from_guid(FormDiagram, guid)

# set anchor points ------------------------------------------------------------
for key in form.vertices_where({'vertex_degree': 2}):
    form.vertex[key]['is_anchor'] = True

# make form diagram ------------------------------------------------------

boundaries = form.vertices_on_boundary()
exterior = boundaries[0]
interior = boundaries[1:]

for key in exterior:
    form.set_vertex_attribute(key, 'is_anchor', True)

form.update_exterior(exterior, feet=1)
form.update_interior(interior)

# set fmins - fmaxs ------------------------------------------------------------

fmin = 20.
fmax = 22.
guids = compas_rhino.get_lines(layer='edges')
edges = compas_rhino.get_line_coordinates(guids)
edges= [[form.gkey_key()[geometric_key(u)], form.gkey_key()[geometric_key(v)]] for u, v in edges]

form.set_edges_attribute('fmin', fmin, edges)
form.set_edges_attribute('fmax', fmax, edges)

# make force diagram -----------------------------------------------------
force = ForceDiagram.from_formdiagram(form)
force.attributes['scale'] = 3.

# horizontal equilibrium -------------------------------------------------------
horizontal(form, force, kmax=100)

# vertical equilibrium ---------------------------------------------------------
vertical_from_formforce_xfunc(form, force)

# rhino drawing ----------------------------------------------------------------
artist = FormArtist(form, layer='FormDiagram')
artist.clear_layer()
artist.draw_vertices(keys=list(form.vertices_where({'is_external': False})))
artist.draw_edges(keys=list(form.edges_where({'is_edge': True, 'is_external': False})))
artist.draw_faces(fkeys=list(form.faces_where({'is_loaded': True})), join_faces=True)

artist.draw_reactions(scale=.5)
artist.draw_forces(scale=.002)

artist.redraw()

artist_ = ForceArtist(force, layer='ForceDiagram')
artist_.clear_layer()
artist_.draw_vertices()
artist_.draw_edges()
artist_.redraw()