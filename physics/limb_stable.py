import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.mathlib.math2d import *
from AML.physics.colliders import *

class Node:
    """
    Represents the joints of limbs

    Nodes are used to define limbs as segments between two points. Nodes also are used
    as the joints that attach limbs to one another.

    Attributes
    ----------
    pos : Vector2
        The center point of the node.

    Methods
    -------
    get_x()
        Returns a value representing the x-coordinate of the node
    set_x(val)
        Sets the value of the x-coordinate of the node
    get_y()
        Returns a value representing the y-coordinate of the node
    set_y(val)
        Sets the value of the y-coordinate of the node
    rotate(angle, pivot)
        Applies a rotation of a given angle about the pivot point to the position
        of the node.
    """
    
    def __init__(self,pos):
        """
        Parameters
        ----------
        pos : Vector2
            The center point of the node.
        """
        
        self.pos = pos
        
    def get_x(self):
        return self.pos.get_x()

    def set_x(self, val):
        self.pos.set_x(val)

    def get_y(self):
        return self.pos.get_y()
    
    def set_y(self, val):
        self.pos.set_y(val)
    
    def rotate(self,angle, pivot):
        self.pos = self.pos.rotate(angle,pivot.pos)
    
class Limb:
    """
    Represents a limb

    A limb is a segment consisting of two nodes and may potentially have attached limbs
    represented as a hierarchy of parents and children.
    When the transform of a parent limb is changed, it cascades down into its children.
    When a child limb encounters a collision and needs to resolve the collision, the
    resulting collision cascades back up to its parents.

    Attributes
    ----------
    nodes : list
        A list of two Node objects defining the location and length of the limb
    children : list
        A list of Limb objects storing the children of the current limb
    parents : dict
        A dict of Limb objects paired with their rotational constraints with respect to
        the current limb storing the parents of the current limb

    Methods
    -------
    rotate_about_child(angle, node)
        Rotates this limb's children 

    """
    
    def __init__(self,n0,n1,numcols,**kwargs):
        if isinstance(n0, Vector2):
            n0 = Node(n0)
        if isinstance(n1, Vector2):
            n1 = Node(n1)
        self.nodes = [n0,n1]
        self.children = kwargs.get('children', [])
        self.parents = kwargs.get('parents', dict())
        self.joints = kwargs.get('joints', [])
        # Produces a limb vector describing the direction and magnitude of the
        # limb.
        lvec = n1.pos - n0.pos
        #radius of individual colliders of the limb
        self.cradius = lvec.mag()/(numcols*2)
        #normalizes the limb vector
        lvec = lvec/lvec.mag()
        #generate colliders to go across the limb
        self.colliders = []
        currpos = n0.pos + lvec*self.cradius
        for i in range(numcols):
            self.colliders.append(CircleCollider(currpos,self.cradius))
            currpos += lvec*(2*self.cradius)
            
    def rotate_about_child(self,angle,node):
        #generate a list of nodes to rotate that are unique to this limb
        #this section removes all nodes that are in both this limb and its children
        rnodes = list(self.nodes)
        for child in self.children:
            for cnode in child.nodes:
                if cnode in rnodes:
                    rnodes.remove(cnode)
        #if the current node is part of this limbs' nodes, delete it as well
        if node in rnodes:
            rnodes.remove(node)
        #rotate all of this limbs' nodes as a parent
        for rnode in rnodes:
            rnode.rotate(angle,node)
        #rotate all of the this limbs's children's
        for child in self.children:
            child.rotate_about_child(angle,node)
        #rotate all of the limb's colliders accordingly
        for col in self.colliders:
            col.pos = col.pos.rotate(angle,node.pos)
            
    def rotate_about(self, angle, node):
        rnodes = list(self.nodes)
        currparent = None
        for parent in self.get_parents():
            if node in parent.nodes:
                currparent = parent
        if(currparent != None and self.parents[parent]):
            constrangle = 45
            nshared = self.get_shared_joint(currparent)
            nself = list(self.nodes)
            nself.remove(nshared)
            nself = nself[0]
            nparent = list(currparent.nodes)
            nparent.remove(nshared)
            nparent = nparent[0]
            s = nself.pos - nshared.pos
            p = nparent.pos - nshared.pos
            currangle = acos((s*p)/(s.mag()*p.mag()))*180/math.pi
            signangle = s.get_x()*p.get_y() - s.get_y()*p.get_x()
            print("Sign = " + str(signangle))
            print("Angle = " + str(angle))
            if angle > 0:
                if(signangle > 0 and currangle - angle <= constrangle):
                    print("Angle pos Less than constr")
                    da = angle - currangle + constrangle
                    angle = angle - da - 0.1
                if(signangle < 0 and currangle + angle >= 180 - constrangle):
                    print("Angle pos Greater than constr")
                    da = currangle + angle - (180 - constrangle)
                    angle = angle - da - 0.1
            elif angle < 0:
                if(signangle > 0 and currangle - angle >= 180 - constrangle):
                    print("Angle neg Greater than constr")
                    da = (currangle - angle) - (180 - constrangle)
                    angle = angle + da + 0.1
                if(signangle < 0 and currangle + angle <= constrangle):
                    print("Angle neg Less than constr")
                    da = constrangle - (angle + currangle) 
                    angle = angle + da + 0.1
                
        for child in self.children:
            for cnode in child.nodes:
                if cnode in rnodes:
                    rnodes.remove(cnode)
        if node in rnodes:
            rnodes.remove(node)
        for rnode in rnodes:
            rnode.rotate(angle,node)
        for child in self.children:
            child.rotate_about_child(angle,node)
        for col in self.colliders:
            col.pos = col.pos.rotate(angle,node.pos)
    
    def translate(self,trans):
        tnodes = list(self.nodes)
        for child in self.children:
            for cnode in child.nodes:
                if cnode in tnodes:
                    tnodes.remove(cnode)
            child.translate(trans)
        for node in tnodes:
            node.pos += trans
        for col in self.colliders:
            col.pos += trans

    def get_node(self,node):
        return self.nodes[node]
    
    def get_collider(self,col):
        return self.colliders[col]
            
    def add_child(self,limb,constraint):
        if not(limb in self.children):
            limb.add_parent(self,constraint)
            for node1 in self.nodes:
                for node2 in limb.nodes:
                    if(node1 == node2):
                        if not(node1 in limb.joints):
                            limb.add_joint(node1)
            self.children.append(limb)
            
    def remove_child(self,limb):
        if limb in self.children:
            limb.parents.remove(self)
            self.children.remove(limb)
            
    def get_parents(self):
        return self.parents.keys()
    
    def add_parent(self,limb,constraint):
        self.parents[limb] = constraint

    '''   
    def add_joint(self,node):
        if not(node in self.joints):
            self.joints.append(node)
            
    def remove_joint(self,node):
        if node in self.joints:
            self.joints.remove(node)
            
    def get_shared_joint(self,limb):
        for node1 in self.nodes:
            for node2 in limb.nodes:
                if(node1 == node2):
                    return node1
        return None
    '''
