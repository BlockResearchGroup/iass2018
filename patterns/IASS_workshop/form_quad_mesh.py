#import time
#
#tic = time.time()
#

import rhinoscriptsyntax as rs

import json
import random
import itertools
import copy

from compas.datastructures import Mesh



from compas.datastructures import Network
from compas.utilities import geometric_key

from compas.topology import depth_first_tree

from compas.geometry import centroid_points
from compas.geometry.algorithms import discrete_coons_patch
from compas.geometry import mesh_cull_duplicate_vertices

from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import scale_vector

from compas.geometry import mesh_smooth_area
from compas.geometry import mesh_smooth_centroid

from compas_rhino import get_line_coordinates
from compas_rhino.conduits import LinesConduit

from compas_rhino import MeshArtist

                
def find_groups(mesh):
    
    num_edges = mesh.number_of_edges()
    
    h_edge_pairs = make_pairs(mesh)
    
    
    seen = set()
    groups = []
    for u,v in mesh.edges():
        
        group = set()
        for h_edge in [(u,v),(v,u)]:
            start = h_edge
            
            if start in seen:
                continue
            
            if start not in h_edge_pairs:
                continue
                    
            group.add((start[0],start[1]))
            group.add((start[1],start[0]))
            count = 0
            while True:

                if h_edge_pairs[start] == None:
                    break
                    
                u,v = h_edge_pairs[start]
                group.add((u,v))
                group.add((v,u))
                
                start = (v,u)
                
                if (v,u) not in h_edge_pairs:
                   break
                
                count += 1
                if count > num_edges:
                    break
        
        if len(group) > 0:
            groups.append(group)
   
        seen = seen.union(group)
        
    edge_groups = []
    for group in groups:
       edges = []
  
       for u,v in group:
           if (u,v) in mesh.edges():
               edges.append((u,v))

       edge_groups.append(edges)
       
    return edge_groups
            
                
def make_pairs(mesh):
    
    h_edge_pairs = {}
    for fkey in mesh.faces():
        h_edges = mesh.face_halfedges(fkey)
        
        if len(h_edges) == 4:
            h_edge_pairs[h_edges[0]] = h_edges[2]
            h_edge_pairs[h_edges[1]] = h_edges[3]
            h_edge_pairs[h_edges[2]] = h_edges[0]
            h_edge_pairs[h_edges[3]] = h_edges[1]
                
        if len(h_edges) == 3:
            
            flag = mesh.get_face_attribute(fkey,'corner')
           

            if flag == 0:
                h_edge_pairs[h_edges[0]] = None
                h_edge_pairs[h_edges[2]] = h_edges[1]
                h_edge_pairs[h_edges[1]] = h_edges[2]
            elif flag == 1:
                h_edge_pairs[h_edges[1]] = h_edges[0]
                h_edge_pairs[h_edges[0]] = h_edges[1]
                h_edge_pairs[h_edges[2]] = None
            elif flag == 2:
                h_edge_pairs[h_edges[2]] = h_edges[0]
                h_edge_pairs[h_edges[1]] = None
                h_edge_pairs[h_edges[0]] = h_edges[2]
                
    return h_edge_pairs

        
def find_devisions(mesh, edge_groups, trg_len):
    
    for edges in edge_groups:
        
        lengths = 0
        for u,v in edges:
            lengths += mesh.get_edge_attribute((u,v),'length')
            
            ave_len = lengths / len(edges)
            div = max((round(ave_len / trg_len,0),1))
            
            
        for u,v in edges:
           crv = mesh.get_edge_attribute((u,v),'guid')
           pts = rs.DivideCurve(crv,div)
           mesh.set_edge_attribute((u,v),'points',pts)
    
    edges = set(mesh.edges())
    coons_meshes = []
    

    
    for fkey in mesh.faces():
           
        h_edges = mesh.face_halfedges(fkey)
            
        # arrange point lists in circular order along edge faces
        pts_coon = []
        for h_edge in h_edges:
            pts = mesh.get_edge_attribute(h_edge,'points')[:]
            if not h_edge in edges:
                pts.reverse()
            if not mesh.get_edge_attribute(h_edge,'dir'):
                pts.reverse()
            pts_coon.append(pts)
            
        # handle triangles correctly based on user input (flag 0 - 2)
        lengths = [len(pts_coon[0]), len(pts_coon[1])]
        if len(h_edges) == 4:
            ab,bc,dc,ad = pts_coon
        else:
            flag = mesh.get_face_attribute(fkey,'corner')
            if flag == 0:
                ab,bc,dc,ad = pts_coon[0],pts_coon[1],[],pts_coon[2]
            elif flag == 1:
                ab,bc,dc,ad = pts_coon[0],[],pts_coon[1],pts_coon[2]
                lengths = [len(pts_coon[0]), len(pts_coon[2])]
            elif flag == 2:
                ab,bc,dc,ad = pts_coon[0],pts_coon[1],pts_coon[2],[]
                
        # reverse for coons patch (see parameters)
        dc.reverse()
        ad.reverse()
            
        
        vertices, faces = discrete_coons_patch(ab,bc,dc,ad)
        coons_meshes.append((vertices, faces, lengths))

    # join al sub "meshes" of the coons patches in one mesh (with duplicate vertices)
    inc = 0
    mesh = Mesh()
    for coons_mesh in coons_meshes:
        vertices, faces, lengths = coons_mesh
        
        a, b = lengths
        
        indices = []
        for i,pt in enumerate(vertices):
            indices.append(i)
            pass
        
   
        
        indices = indices[::b] + indices[b-1::b]+ indices[:b] + indices[(a-1)*b:]
        indices = set(indices)
        
        
        for i,pt in enumerate(vertices):
            if i in indices:
                attr = {'coon_bound' : True}
            else:
                attr = {'coon_bound' : False}
            mesh.add_vertex(i + inc, x=pt[0], y=pt[1], z=pt[2], attr_dict=attr)
        
        for face in faces:
            face = [key + inc for key in face]
            mesh.add_face(face)
        inc += len(vertices)
        
    
    return mesh
    

def set_tri_corners(mesh):
    
    dots = {}
    rs.EnableRedraw(False)
    
    for fkey in mesh.faces():
        c_pts = mesh.face_coordinates(fkey)
        # reverse oder to make the flags match with the corners
        c_pts.reverse()
        if len(c_pts) != 3:
            continue
        
        cent = mesh.face_centroid(fkey)
        
        for i,c_pt in enumerate(c_pts):
            pt = centroid_points([cent,c_pt])
            dot = rs.AddTextDot('', pt)
            rs.TextDotHeight(dot,6)
            dots[str(dot)] = (fkey,i)
    
    
    rs.EnableRedraw(True)
    if not dots:
        return None
    
    dot_ids = dots.keys()
    
    
    data = rs.GetObjectsEx(message="Select face dot", filter=0, preselect=False, select=False, objects=dot_ids)
    
    rs.DeleteObjects(dot_ids)
    if not data:
        return None
    
    for datum in data:
        dot = datum[0]
        fkey, flag = dots[str(dot)] 
        if flag == None:
            return None
        mesh.set_face_attribute(fkey,'corner',flag)
    
    return True

def lines_from_mesh(mesh):
    return [mesh.edge_coordinates(u,v) for u,v in mesh.edges()]

def group_and_mesh(mesh, trg_len):
    edge_groups = find_groups(mesh)
    coons_mesh = find_devisions(mesh, edge_groups, trg_len)
    return coons_mesh

def mesh_cull_duplicate_vertices(mesh, precision='3f'):
    """Cull all duplicate vertices of a mesh and sanitize affected faces.

    Parameters
    ----------
    mesh : Mesh
        A mesh object.
    precision (str): Optional.
        A formatting option that specifies the precision of the
        individual numbers in the string (truncation after the decimal point).
        Supported values are any float precision, or decimal integer (``'d'``).
        Default is ``'3f'``.
    """

    geo_keys = {}
    keys_geo = {}
    keys_pointer = {}
    for key in mesh.vertices():
        geo_key = geometric_key(mesh.vertex_coordinates(key), precision)
        if geo_key in geo_keys:
            keys_pointer[key] = geo_keys[geo_key]
        else:
            geo_keys[geo_key] = key
            keys_geo[key] = geo_key

    keys_remain = geo_keys.values()
    keys_del = [key for key in mesh.vertices() if key not in keys_remain]

    # delete vertices
    for key in keys_del:
        del mesh.vertex[key]

    # sanitize affected faces
    new_faces = {}
    for fkey in mesh.faces():
        face = []
        seen = set()
        for key in mesh.face_vertices(fkey):
            if key in keys_pointer:
                pointer = keys_pointer[key]
                if pointer not in seen:
                    face.append(pointer)
                    seen.add(pointer)
            else:
                face.append(key)
        if seen:
            new_faces[fkey] = face

    for fkey in new_faces:
        mesh.delete_face(fkey)
        mesh.add_face(new_faces[fkey], fkey)

def get_initial_mesh(precision):
    
    
    
    crvs = rs.GetObjects("Select boundary curves", 4, group=True, preselect=False, select=False, objects=None, minimum_count=3, maximum_count=0)
    lines = get_line_coordinates(crvs)
    geo_lines = [(geometric_key(pt_u,precision), geometric_key(pt_v,precision)) for pt_u, pt_v in lines]
    network = Network.from_lines(lines, precision)
   
    if network.leaves(): 
        return None
        
    adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}
    root = network.get_any_vertex()
    ordering, predecessors, paths = depth_first_tree(adjacency, root)
    if len(ordering) != network.number_of_vertices():
        return None
    
    mesh = Mesh.from_lines(lines, delete_boundary_face=True, precision=precision)
    
    rs.EnableRedraw(False)
    
    dots = {}
    for fkey in mesh.faces():
        cent = mesh.face_centroid(fkey)

        dot = rs.AddTextDot('', cent)
        rs.TextDotHeight(dot,6)
        dots[str(dot)] = fkey
    rs.EnableRedraw(True)
    if not dots:
        return None
    
    dot_ids = dots.keys()
    
    
    data = rs.GetObjectsEx(message="Select face for openings", filter=0, preselect=False, select=False, objects=dot_ids)
    
    rs.DeleteObjects(dot_ids)
    
    if data:
        for datum in data:
            dot = datum[0]
            fkey = dots[str(dot)]         
            mesh.delete_face(fkey)
        
    
    geo_edges = []
    for u,v, attr in mesh.edges(True):
        pt_u, pt_v = mesh.edge_coordinates(u,v)
        geo_u, geo_v = geometric_key(pt_u,precision), geometric_key(pt_v,precision)
        for i, geo_l_uv in enumerate(geo_lines):
            geo_l_u, geo_l_v = geo_l_uv[0], geo_l_uv[1]
            if (geo_l_u == geo_u) and (geo_l_v == geo_v):
                attr['dir'] = True
            elif (geo_l_u == geo_v) and (geo_l_v == geo_u):
                attr['dir'] = False
            else: continue
            attr['guid'] = str(crvs[i])
            attr['length'] = rs.CurveLength(crvs[i])
                
    # initiate flag for corners
    for fkey, attr in mesh.faces(True):
        mesh.set_face_attribute(fkey,'corner',0)
        
    return mesh, crvs

        
    
if __name__ == '__main__':
    
    #user inputs
    #----------------------------------------
    #----------------------------------------
    precision = '3f'
    trg_len = 0.75
    mesh, crvs = get_initial_mesh(precision)
    #----------------------------------------
    #----------------------------------------
    
    coons_mesh = group_and_mesh(mesh, trg_len)
    mesh_lines = lines_from_mesh(coons_mesh)
    
    try:
        conduit = LinesConduit(mesh_lines)
        conduit.Enabled = True
     
        while True:
            if not set_tri_corners(mesh):
                break
            if not trg_len:
                break
                
            coons_mesh = group_and_mesh(mesh, trg_len)
            mesh_lines = lines_from_mesh(coons_mesh)
            conduit.lines = mesh_lines
            conduit.redraw()
            
    except Exception as e:
        print(e)
        
    finally:
        conduit.Enabled = False
        del conduit
        
    
    mesh_cull_duplicate_vertices(coons_mesh, precision)
    
    #fixed = coons_mesh.vertices_on_boundary()
    #mesh_smooth_area(coons_mesh, fixed=fixed, kmax=25,damping=0.5)
    #mesh_smooth_centroid(coons_mesh, fixed=fixed, kmax=5,damping=0.5)
    
    artist = MeshArtist(coons_mesh, layer='form_quad')
    artist.draw_edges()
    artist.draw_vertices()
    #artist.draw_faces()
    artist.redraw()
