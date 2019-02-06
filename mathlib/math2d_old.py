import math
class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __getitem__(self, key):
        if(key == 0):
            return self.x
        elif(key == 1):
            return self.y
        else:
            raise IndexError("vector index out of range")
    def __setitem__(self, key, value):
        if(key == 0):
            self.x = value
        elif(key == 1):
            self.y = value
        else:
            raise IndexError("vector index out of range")
    def mag(self):
        return math.sqrt(self.x**2+self.y**2)
    def rotate(self,*args):
        angle = args[0]*math.pi/180
        rmat = Matrix2(math.cos(angle),-math.sin(angle),math.sin(angle),
                           math.cos(angle))
        if len(args) == 1:
            #print(rmat*self)
            return rmat*self
        elif len(args) == 2:
            pivot = args[1]
            sprime = self - pivot
            sprime = rmat*sprime
            sprime = sprime + pivot
            #print(sprime)
            return sprime
        else:
            raise TypeError("rotate() takes at most 2 arguments(" +
                            str(len(args))+ " given)")
    def __neg__(self):
        return Vector2(-self.x,-self.y)
    def __add__(self,other):
        res = Vector2(0,0)
        if isinstance(other,Vector2):
            res.x = self.x + other.x
            res.y = self.y + other.y
        else:
            res.x = self.x + other
            res.y = self.y + other
        return res
    def __sub__(self,other):
        other = -other
        return self + other
    def __mul__(self,other):
        if isinstance(other,Vector2):
            return self.x * other.x + self.y * other.y
        else:
            res = Vector2(0,0)
            res.x = self.x * other
            res.y = self.y * other
        return res
    def __truediv__(self,other):
        res = Vector2(0,0)
        if isinstance(other,Vector2):
            res.x = self.x / other.x
            res.y = self.y / other.y
        else:
            res.x = self.x / other
            res.y = self.y / other
        return res
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y
    def __neq__(self,other):
        return not (self == other)
    def __lt__(self,other):
        return (self.x < other.x and self.y < other.y)
    def __le__(self,other):
        return (self.x <= other.x and self.y <= other.y)
    def __gt__(self,other):
        return (self.x > other.x and self.y > other.y)
    def __ge__(self,other):
        return (self.x >= other.x and self.y >= other.y)
    def __repr__(self):
        return str((self.x,self.y))
    
class Matrix2:
    def __init__(self,*args):
        self.m = [[0,0] for i in range(2)]
        arglen = len(args)
        if arglen == 0:
            pass
        elif arglen == 1:
            self.m = args[0]
        elif arglen == 2:
            for i in range(2):
                self.m[i] = [args[i][0],args[i][1]]
        elif arglen == 4:
            self.m = [[args[0],args[1]],[args[2],args[3]]]
        else:
            raise Exception("invalid number of parameters")
    def __getitem__(self, key):
        if(key <= 1 and key >= -2):
            return self.m[key]
        else:
            raise IndexError("row index out of range")
    def __setitem__(self, key, value):
        if(key <= 1 and key >= -2):
            self.m[key] = value
        else:
            raise IndexError("row index out of range")
    def __mul__(self,other):
        if isinstance(other, Vector2):
            x = self.m[0][0]*other.x + self.m[0][1]*other.y
            y = self.m[1][0]*other.x + self.m[1][1]*other.y
            return Vector2(x,y)
        elif isinstance(other, int) or isinstance(other, float):
            retm = Matrix2()
            for i in range(2):
                for j in range(2):
                    retm[i][j] = self[i][j] * other
            return retm
        else:
            retm = Matrix2()
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        retm[i][j] += self[i][k]*other[k][j]
            return retm
    def __add__(self,other):
        retm = Matrix2()
        for i in range(2):
            for j in range(2):
                retm[i][j] = self[i][j] + other[i][j]
        return retm
    def __sub__(self,other):
        retm = Matrix2()
        for i in range(2):
            for j in range(2):
                retm[i][j] = self[i][j] - other[i][j]
        return retm
    def __repr__(self):
        return str(self.m)

def acos(x):
     return math.acos(min(1,max(x,-1)))
    
            
