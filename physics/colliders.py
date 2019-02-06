import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.mathlib.math2d import*

class CollisionInstance:
    """
    Represents the vectors describing collisions.

    Represents the vector along which the collision occurred and
    the vector that describes how far along the vector the collision is.
    To resolve the collision, simply set the pos to (pos - coldepth).

    Attributes
    ----------
    colvec : Vector2
        The vector along which the collision occurred
    coldepth : Vector2
        A scaled version of colvec that represents the depth of the collision

    Methods
    -------
    None
    """
    
    def __init__(self,colvec,coldepth):
        """
        Parameters
        ----------
        colvec : Vector2
            The vector along which the collision occurred.
        coldepth : Vector2
            A scaled version of colvec that represents the depth of the collision
        """
        
        self.colvec = colvec
        self.coldepth = coldepth
        
    def __repr__(self):
        return (str((self.colvec.get_x(),self.colvec.get_y()))
                + ", " + str((self.coldepth.get_x(),self.coldepth.get_y())))

class CircleCollider:
    """
    A collider defined by a position and a radius

    Checks for collisions about a central point about a given radius

    Attributes
    ----------
    pos : Vector2
        The center point of the collider
    radius : float
        The length of the radius
    is_colliding: bool
        Represents the state of the collider as either colliding or not colliding

    Methods
    -------
    get_collision(other)
        Returns a tuple with a boolean and CollisionInstance indicating if and where
        a collision has occurred with another collider
    """
    
    def __init__(self,pos,radius,**kwargs):
        """
        Parameters
        ----------
        pos : Vector2
            The center point of the collider
        radius : float
            The length of the radius
        is_colliding: bool
            Represents the state of the collider as either colliding or not colliding
        """
        
        self.pos = pos
        self.radius = radius
        ##self.sout = kwargs.get('sout',[])
        self.is_colliding = kwargs.get('is_colliding',False)

    def get_collision(self,other):
        """
        Returns the collision occuring between this collider and another if it exists.

        Parameters
        ----------
        pos : Vector2
            The center point of the collider
        radius : float
            The length of the radius
        is_colliding: bool
            Represents the state of the collider as either colliding or not colliding

        Returns
        -------
        tuple
            (boolean hasCollided, CollisionInstance collision)
            If hasCollided is False then collision will be None
        """
        
        # If we are getting a collision with another circle collider,
        # then compare the distance between the centers of the two colliders
        # and if the distance is less than the sum of their radii, they collide.
        if isinstance(other, CircleCollider):
            if (self.pos - other.pos).mag() < (self.radius + other.radius):
                colvecs = other.pos - self.pos
                colveco = -colvecs
                colvecsu = colvecs/colvecs.mag()
                colvecou = colveco/colveco.mag()
                colvecsr = colvecsu*self.radius + self.pos
                colvecor = colvecou*other.radius + other.pos
                coldepth = colvecsr - colvecor
                self.is_colliding = True
                return (True, CollisionInstance(colvecs,coldepth))
            else:
                return (False, None)

        # Otherwise, if we are getting a collision with a surface collider:
        elif isinstance(other, SurfaceCollider):
            
            # First we check if the surface collider is entirely vertical or entirely
            # horizontal.
            if(((other.p1.get_x() == other.p2.get_x()) and
                                            ((self.pos.get_y() >= other.p1.get_y() and
                                               self.pos.get_y() >= other.p2.get_y()) or
                                               (self.pos.get_y() <= other.p1.get_y() and
                                               self.pos.get_y() <= other.p2.get_y())))
               or
               ((other.p1.get_y() == other.p2.get_y()) and ((self.pos.get_x() >= other.p1.get_x() and
                                               self.pos.get_x() >= other.p2.get_x()) or
                                               (self.pos.get_x() <= other.p1.get_x() and
                                               self.pos.get_x() <= other.p2.get_x())))):
                
                # If this is true, we get the closest of the two points of the surface collider.
                # Then we check if the distance between the circle collider and that point is less
                # than the radius of the circle collider and return a collision if it is.
                vsc = other.get_closest(self.pos)
                colvec = vsc - self.pos
                if(colvec.mag() < self.radius):
                    coldepth = -(colvec - (colvec/colvec.mag())*self.radius)
                    self.is_colliding = True
                    return (True, CollisionInstance(colvec,coldepth))
                else:
                    return (False, None)

            # Otherwise, we check for diagonal orientations of the collision surface where the
            # circle collider is entirely to the left or the right and entirely above or below the
            # collision surface and do the same as we did before.
            elif(((self.pos.get_x() < other.p1.get_x() and self.pos.get_x() < other.p2.get_x()) or
                  (self.pos.get_x() > other.p1.get_x() and self.pos.get_x() > other.p2.get_x()))
                 and
                 ((self.pos.get_y() > other.p1.get_y() and self.pos.get_y() > other.p2.get_y()) or
                   (self.pos.get_y() < other.p1.get_y() and self.pos.get_y() < other.p2.get_y()))):
                vsc = other.get_closest(self.pos)
                colvec = vsc - self.pos
                if(colvec.mag() < self.radius):
                    coldepth = -(colvec - (colvec/colvec.mag())*self.radius)
                    self.is_colliding = True
                    return (True,CollisionInstance(colvec,coldepth))
                else:
                    return (False,None)
                
            # The only remaining case is if the surface collider is diagonal and the circle collider is
            # between the two points of the surface collider in the x or y direction or both
            else:
                
                # In this case, we check the normal between the surface collider and the center of the
                # circle collider. If the length of the normal is less than the radius of the circle
                # collider, then a collision has occurred.
                a = self.pos - other.p2
                b = other.p2 - other.p1
                ap = a - b*((a*b)/(b*b))
                if ap.mag() < self.radius:
                    colvec = -ap
                    coldepth = -(colvec - (colvec/colvec.mag())*self.radius)
                    self.is_colliding = True
                    return (True,CollisionInstance(colvec,coldepth))
                else:
                    return (False,None)
        else:
            return (False,None)

    '''
    def update_synapse(self):
        if(self.is_colliding):
            for s in self.sout:
                s.value = s.potential*s.sign
        else:
            for s in self.sout:
                s.value = 0
        self.is_colliding = False
        
    def add_sout(self,synapse):
        self.sout.append(synapse)
        
    def remove_sout(self,synapse):
        if(synapse in self.sout):
            del(self.sout[index(synapse)])
    '''
    
class SurfaceCollider:
    """
    A collider defined as a line segment between two points

    The line segment acts as a surface for other colliders to collide with

    Attributes
    ----------
    p1 : Vector2
        The first anchor point of the line segment representing the collider
    p2 : Vector2
        The second anchor point of the line segment representing the collider

    Methods
    -------
    get_closest(pos)
        Returns the closer of the surface's two anchor points to a given position.
    """
    
    def __init__(self,p1,p2):
        """
        Parameters
        ----------
        p1 : Vector2
            The first anchor point of the line segment representing the collider
        p2 : Vector2
            The second anchor point of the line segment representing the collider
        """
        
        self.p1 = p1
        self.p2 = p2
    def get_closest(self,pos):
        """
        Returns the closer of the surface's two anchor points to a given position.

        Parameters
        ----------
        pos : Vector2
            The position for which we want to find the closer point.

        Returns
        -------
        Vector2
            The closer of the two anchor points of the surface.
        """
        
        if((self.p1-pos).mag() <= (self.p2-pos).mag()):
            return self.p1
        else:
            return self.p2
    
