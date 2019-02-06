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
    as the joints that attach limbs to one another

    Attributes
    ----------
    pos : Vector2
        The center point of the node

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
        of the node
    """
    
    def __init__(self,pos):
        """
        Parameters
        ----------
        pos : Vector2
            The center point of the node
        """
        
        self.pos = pos
        
    def get_x(self):
        """
        Returns the x-coordinate of this node

        Returns
        -------
        float
            A number representing the x-coordinate
        """
        
        return self.pos.get_x()

    def set_x(self, val):
        """
        Sets the x-coordinate of this node

        Parameters
        ----------
        val : float
            The value to set the x-coordinate to
        """
        
        self.pos.set_x(val)

    def get_y(self):
        """
        Returns the y-coordinate of this node

        Returns
        -------
        float
            A number representing the y-coordinate
        """
        
        return self.pos.get_y()
    
    def set_y(self, val):
        self.pos.set_y(val)
        """
        Sets the y-coordinate of this node

        Parameters
        ----------
        val : float
            The value to set the y-coordinate to
        """
    
    def rotate(self, angle, pivot):
        """
        Rotates this node by a given angle about a pivot

        Parameters
        ----------
        angle : float
            The angle by which to rotate
        pivot : Vector2
            The vector specifying the pivot location
        """
        self.pos = self.pos.rotate(angle,pivot.pos)
    
class Limb:
    """
    Represents a limb.

    A limb is a segment consisting of two nodes and may potentially have attached limbs
    represented as a hierarchy of parents and children.
    When the transform of a parent limb is changed, it cascades down into its children.

    Attributes
    ----------
    nodes : list
        A list of two Node objects defining the location and length of the limb.
    children : list
        A list of Limb objects storing the children of the current limb.
    parents : dict
        A dict of Limb objects with a parent relationship to the current limb paired with their
        rotational constraints with respect to the current limb.

    Methods
    -------
    rotate_child_about(angle, node)
        Called exclusively on the children of the Limb to be rotated. Rotates a child limb
        and its respective children recursively.
    rotate_about(angle, node)
        Called on the Limb instance. Rotates a limb about one of its two nodes at the specified
        angle.
    translate(trans)
        Translates the limb and its child limbs by the specified vector trans.
    get_node(node)
        Returns the node of the specified number, node.
    get_collider(self, col):
        Returns the collider of the specified number, col.         
    add_child(self, limb, constraint):
        Adds the specified limb, limb, as a child to the current limb and adds the current limb
        as a parent to the specified limb, limb, with the specified constraint, constraint.
    remove_child(self, limb)
         Removes the specified child, limb.
    get_parents(self)
        Returns the parent nodes of the current limb.
    add_parent(self, limb, constraint)
        Adds a the specified limb, limb, as a parent to the current limb with the specified constraint,
        constraint, and adds the current limb to the specified limb as a child.
    get_shared_joint(self, limb)
        Returns the shared joint between this limb and the specified limb, limb, as a node.
    """
    
    def __init__(self,n0,n1,numcols,**kwargs):
        if isinstance(n0, Vector2):
            n0 = Node(n0)
        if isinstance(n1, Vector2):
            n1 = Node(n1)
        self.nodes = [n0,n1]
        self.children = kwargs.get('children', [])
        self.parents = kwargs.get('parents', dict())
        # Produces a limb vector describing the direction and magnitude of the limb
        lvec = n1.pos - n0.pos
        # Radius of each of the colliders of the limb
        self.cradius = lvec.mag()/(numcols*2)
        # Normalizes the limb vector
        lvec = lvec/lvec.mag()
        # Generate colliders to go across the limb
        self.colliders = []
        currpos = n0.pos + lvec*self.cradius
        for i in range(numcols):
            self.colliders.append(CircleCollider(currpos,self.cradius))
            currpos += lvec*(2*self.cradius)
            
    def rotate_child_about(self, angle, node):
        # Generate a list of nodes to rotate that are unique to this limb
        # this section removes all nodes that are in both this limb and its children
        rnodes = list(self.nodes)
        for child in self.children:
            for cnode in child.nodes:
                if cnode in rnodes:
                    rnodes.remove(cnode)
        # If the current node is part of this limbs' nodes, delete it as well
        if node in rnodes:
            rnodes.remove(node)
        # Rotate all of this limbs' nodes as a parent
        for rnode in rnodes:
            rnode.rotate(angle, node)
        # Rotate all of the this limbs's children's
        for child in self.children:
            child.rotate_child_about(angle, node)
        # Rotate all of the limb's colliders accordingly
        for col in self.colliders:
            col.pos = col.pos.rotate(angle, node.pos)
            
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
            ##print("Sign = " + str(signangle))
            ##print("Angle = " + str(angle))
            if angle > 0:
                if(signangle > 0 and currangle - angle <= constrangle):
                    ##print("Angle pos Less than constr")
                    da = angle - currangle + constrangle
                    angle = angle - da - 0.1
                if(signangle < 0 and currangle + angle >= 180 - constrangle):
                    ##print("Angle pos Greater than constr")
                    da = currangle + angle - (180 - constrangle)
                    angle = angle - da - 0.1
            elif angle < 0:
                if(signangle > 0 and currangle - angle >= 180 - constrangle):
                    ##print("Angle neg Greater than constr")
                    da = (currangle - angle) - (180 - constrangle)
                    angle = angle + da + 0.1
                if(signangle < 0 and currangle + angle <= constrangle):
                    ##print("Angle neg Less than constr")
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
            child.rotate_child_about(angle, node)
        for col in self.colliders:
            col.pos = col.pos.rotate(angle, node.pos)
    
    def translate(self, trans):
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

    def get_node(self, node):
        return self.nodes[node]
    
    def get_collider(self, col):
        return self.colliders[col]
            
    def add_child(self, limb, constraint):
        if limb not in self.children:
            self.children.append(limb)
        limb.parents[self] = constraint
            
    def remove_child(self, limb):
        if limb in self.children:
            limb.parents.remove(self)
            self.children.remove(limb)
            
    def get_parents(self):
        return self.parents.keys()
    
    def add_parent(self, limb, constraint):
        self.parents[limb] = constraint
        if self not in limb.children:
            limb.children.append(self)
            
    def get_shared_joint(self, limb):
        for node1 in self.nodes:
            for node2 in limb.nodes:
                if(node1 == node2):
                    return node1
        return None
