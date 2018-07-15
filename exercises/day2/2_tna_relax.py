from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.utilities import XFunc

from compas_rhino.utilities import get_meshes
from compas_rhino.helpers import mesh_from_guid

from compas_tna.diagrams import FormDiagram
from compas_tna.diagrams import ForceDiagram

from compas_tna.equilibrium import horizontal_rhino as horizontal
from compas_tna.equilibrium import vertical_from_zmax_rhino as vertical_from_zmax
from compas_tna.equilibrium import vertical_from_self_rhino as vertical_from_self
from compas_tna.equilibrium import vertical_from_formforce_rhino as vertical_from_formforce

from compas_tna.rhino import FormArtist
from compas_tna.rhino import ForceArtist

__author__    = ['Tom Van Mele', 'Tomas Mendez Echenagucia']
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


# ------------------------------------------------------------------------------
# make form diagram from rhino mesh
# ------------------------------------------------------------------------------
guid = get_meshes(layer='mesh')[0]
form = mesh_from_guid(FormDiagram, guid)

# find mesh boundaries ---------------------------------------------------------
boundaries = form.vertices_on_boundaries()
exterior = boundaries[0]
interior = boundaries[1:]

# set anchor points ------------------------------------------------------------
for key in form.vertices_where({'vertex_degree': 2}):
    form.vertex[key]['is_anchor'] = True

# relax form diagram -----------------------------------------------------------
form.set_edges_attribute('q', 15, keys=form.edges_on_boundary())
form.relax(fixed=form.vertices_where({'vertex_degree': 2}))

# pre-process / feet-making ----------------------------------------------------
form.update_exterior(exterior, feet=2)
form.update_interior(interior)

# ------------------------------------------------------------------------------
# make force diagram
# ------------------------------------------------------------------------------
force = ForceDiagram.from_formdiagram(form)

# ------------------------------------------------------------------------------
# horizontal equilibrium
# ------------------------------------------------------------------------------
horizontal(form, force, kmax=100)

# ------------------------------------------------------------------------------
# vertical equilibrium
# ------------------------------------------------------------------------------
vertical_from_zmax(form, force, zmax=5.)
vertical_from_self(form, force)
vertical_from_formforce(form, force)

# ------------------------------------------------------------------------------
# rhino drawings
# ------------------------------------------------------------------------------

# form diagram -----------------------------------------------------------------
artist = FormArtist(form, layer='FormDiagram')
artist.clear_layer()
artist.draw_vertices(keys=list(form.vertices_where({'is_external': False})))
artist.draw_edges(keys=list(form.edges_where({'is_edge': True, 'is_external': False})))
artist.draw_faces(fkeys=list(form.faces_where({'is_loaded': True})), join_faces=True)
artist.draw_reactions(scale=.1)
artist.draw_forces(scale=.003)
artist.redraw()

# force diagram ----------------------------------------------------------------
artist_ = ForceArtist(force, layer='ForceDiagram')
artist_.clear_layer()
artist_.draw_vertices()
artist_.draw_edges()
artist_.redraw()
