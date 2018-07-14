from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import random

import compas
import compas_ags

from compas_ags.diagrams import FormDiagram
from compas_ags.diagrams import ForceDiagram

from compas_ags.viewers import Viewer

from compas_ags.ags import graphstatics as gs


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


form = FormDiagram.from_obj(compas.get('lines.obj'))
force = ForceDiagram.from_formdiagram(form)


viewer = Viewer(form, force, delay_setup=False)

viewer.draw_form(
    vertexsize=0.15,
    vertexlabel={key: key for key in form.vertices()},
    edgelabel={uv: index for index, uv in enumerate(form.edges())},
    external_on=True
)

viewer.draw_force(
    vertexsize=0.15,
    vertexlabel={key: key for key in force.vertices()}
)

viewer.show()
