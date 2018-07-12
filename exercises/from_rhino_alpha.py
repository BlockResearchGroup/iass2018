from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas_rhino.utilities import XFunc
from compas_rhino.utilities import get_meshes
from compas_rhino.helpers import mesh_from_guid

from compas.utilities import pairwise
from compas.utilities import flatten

from compas_tna.rhino import RhinoFormDiagram
from compas_tna.rhino import RhinoForceDiagram

horizontal_nodal = XFunc('compas_tna.equilibrium.horizontal_nodal_xfunc')
vertical_from_zmax = XFunc('compas_tna.equilibrium.vertical_from_zmax_xfunc')


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

# make rhino from diagram ------------------------------------------------------
boundaries = form.vertices_on_boundary()
exterior = boundaries[0]
interior = boundaries[1:]

#form.set_edges_attribute('q', 3.0, keys=form.edges_on_boundary())
#form.relax(fixed=form.vertices_where({'vertex_degree': 2}))

form.update_exterior(exterior, feet=2)
form.update_interior(interior)

# make rhino force diagram -----------------------------------------------------
force = RhinoForceDiagram.from_formdiagram(form)

# horizontal equilibrium -------------------------------------------------------
formdata, forcedata = horizontal_nodal(form.to_data(), force.to_data(), kmax=100, alpha=95)

# vertical equilibrium ---------------------------------------------------------
formdata, forcedata = vertical_from_zmax(formdata, forcedata, zmax=3, display=False)
form.data = formdata
force.data = forcedata

# rhino drawing ----------------------------------------------------------------
form.draw()
force.draw()
