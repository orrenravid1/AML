import math

class Vector:
    def __init__(self, arg):

        '''
        A Vector can be initialized from:
        Vector - from which the elements will be copied
        list or tuple - from which elements will be copied
        int - a size that specifies the dimension of a Vector of zeros
        '''
        
        if isinstance(arg, Vector):
            self.v = arg.v.copy()
        elif isinstance(arg, list):
            self.v = arg
        elif isinstance(arg, tuple):
            self.v = list(arg)
        elif isinstance(arg, int):
            self.v = [0 for _ in range(arg)]
        else:
            raise TypeError("Vector only accepts arguments of type Vector, int, tuple or list")

    def __len__(self):
        return len(self.v)

    def __getitem__(self, key):
        if(key >= 0 and key < len(self)):
            return self.v[key]
        else:
            raise IndexError("Vector index out of range")

    def __setitem__(self, key, value):
        if (key >= 0 and key < len(self)):
            self.v[key] = value
        else:
            raise IndexError("Vector index out of range")

    def mag(self):
        s = 0
        for i in range(len(self)):
            s += self.v[i]**2;
        s = math.sqrt(s)
        return s

    def normalized(self):
        return Vector(self/self.mag())
    
    def __neg__(self):
        vnew = self.v;
        for i in range(len(self)):
            vnew[i] = -vnew[i]
        return Vector(vnew)

    def __add__(self, other):
        retv = Vector([0 for i in range(len(self))])
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError("Vector dimensions do not match")
            for i in range(len(self)):
                retv.v[i] = self.v[i] + other.v[i]
        else:
            for i in range(len(self)):
                retv.v[i] = self.v[i] + other
        return retv

    def __sub__(self, other):
        other = -other
        return self + other

    def __mul__(self, other):
        retv = Vector([0 for i in range(len(self))])
        if isinstance(other, Vector):
            if len(self) != len(self):
                raise ValueError("Vector dimensions do not match")
            for i in range(len(self)):
                retv.v[i] = self.v[i] * other.v[i]
        else:
            for i in range(len(self)):
                retv.v[i] = self.v[i] * other
        return retv

    def __truediv__(self, other):
        retv = Vector([0 for i in range(len(self))])
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError("Vector dimensions do not match")
            for i in range(len(self)):
                retv.v[i] = self.v[i] / other.v[i]
        else:
            for i in range(len(self)):
                retv.v[i] = self.v[i] / other
        return retv

    def __eq__(self, other):
        if len(self) != len(other):
            raise ValueError("Vector dimensions do not match")
        ret = True
        for i in range(len(self)):
            ret = ret and (self.v[i] == other.v[i])
        return ret

    def __neq__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if len(self) != len(other):
            raise ValueError("Vector dimensions do not match")
        ret = True
        for i in range(len(self)):
            ret = ret and (self.v[i] < other.v[i])
        return ret

    def __le__(self, other):
        if self.dim != len(other):
            raise ValueError("Vector dimensions do not match")
        ret = True
        for i in range(len(self)):
            ret = ret and (self.v[i] <= other.v[i])
        return ret

    def __gt__(self, other):
        if len(self) != len(other):
            raise ValueError("Vector dimensions do not match")
        ret = True
        for i in range(self.dim):
            ret = ret and (self.v[i] > other.v[i])
        return ret

    def __ge__(self, other):
        if len(self) != len(other):
            raise ValueError("Vector dimensions do not match")
        ret = True
        for i in range(len(self)):
            ret = ret and (self.v[i] >= other.v[i])
        return ret

    def __repr__(self):
        rep = tuple([vec for vec in self.v])
        return str(rep)

class Matrix:
    def __init__(self, *args, **kwargs):
        d = "dim"
        self.rows = kwargs.get("rows",2)
        self.cols = kwargs.get("cols",2)
        if d in kwargs:
            self.rows = kwargs[d][0]
            self.cols = kwargs[d][1]
            self.m = [[0 for i in range(self.cols)] for j in range(self.rows)]
        else:
            self.m = [[0, 0] for i in range(2)]
        arglen = len(args)
        if arglen == 0:
            pass
        elif arglen == 1:
            self.m = args[0]
        else:
            raise Exception("invalid number of parameters")

    def __getitem__(self, key):
        if (key >= 0 and key < self.rows):
            return self.m[key]
        else:
            raise IndexError("row index out of range")

    def __setitem__(self, key, value):
        if (key >= 0 and key < self.rows):
            self.m[key] = value
        else:
            raise IndexError("row index out of range")

    def __mul__(self, other):
        if isinstance(other, Vector):
            if other.dim != self.cols:
                raise ValueError("size of matrix columns does not match vector dimension")
            res = [0 for i in range(self.cols)]
            s = 0
            for i in range(self.rows):
                for j in range(self.cols):
                    s += self.m[i][j]*other.v[j]
                res[i] = s
            return Vector(res)
        elif isinstance(other, int) or isinstance(other, float):
            retm = Matrix()
            for i in range(self.rows):
                for j in range(self.cols):
                    retm[i][j] = self[i][j] * other
            return retm
        else:
            retm = Matrix()
            for i in range(self.rows):
                for j in range(other.cols):
                    for k in range(self.cols):
                        retm[i][j] += self[i][k] * other[k][j]
            return retm

    def __add__(self, other):
        retm = Matrix()
        for i in range(self.rows):
            for j in range(self.cols):
                retm[i][j] = self[i][j] + other[i][j]
        return retm

    def __sub__(self, other):
        retm = Matrix()
        for i in range(self.rows):
            for j in range(self.cols):
                retm[i][j] = self[i][j] - other[i][j]
        return retm

    def __repr__(self):
        return str(self.m)

class Basis:
    def __init__(self, vectors):
        self.vectors = vectors

    def __len__(self):
        return len(self.vectors)

    def vectorBasis(self, vector):
        if self.dim != vector.dim:
            raise ValueError("Vector dimension does not match Basis dimension")
        else:
            vbasis = Vector([0 for i in range(self.dim)])
            for i in range(self.dim):
                vbasis = vbasis + self.vectors[i]*vector
            return vbasis

    def compoundVector(self):
        vtot = Vector([0 for i in range(self.dim)])
        for i in range(self.dim):
            vtot = vtot + self.vectors[i]
        return vtot

    def basisVectors(self):
        return self.vectors

class Vector2(Vector):
    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])
        elif len(args) == 2:
            self.v = [args[0],args[1]]
            
    def get_x(self):
        return self.v[0]
    
    def get_y(self):
        return self.v[1]
    
    def set_x(self, val):
        self.v[0] = val

    def set_y(self, val):
        self.v[1] = val
        
    def rotate(self, *args):
        angle = args[0] * math.pi / 180
        rmat = Matrix2(math.cos(angle), -math.sin(angle), math.sin(angle),
                       math.cos(angle))
        if len(args) == 1:
            return rmat * self
        elif len(args) == 2:
            pivot = args[1]
            sprime = self - pivot
            sprime = rmat * sprime
            sprime = sprime + pivot
            return sprime
        else:
            raise TypeError("rotate() takes at most 2 arguments(" +
                            str(len(args)) + " given)")

    def __neg__(self):
        return Vector2(-self.get_x(), -self.get_y())

    def __add__(self, other):
        res = Vector2(0, 0)
        if isinstance(other, Vector2):
            res.set_x(self.get_x() + other.get_x())
            res.set_y(self.get_y() + other.get_y())
        else:
            res.set_x(self.get_x() + other)
            res.set_y(self.get_y() + other)
        return res

    def __sub__(self, other):
        other = -other
        return self + other

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return self.get_x() * other.get_x() + self.get_y() * other.get_y()
        else:
            res = Vector2(0, 0)
            res.set_x(self.get_x() * other)
            res.set_y(self.get_y() * other)
        return res

    def __truediv__(self, other):
        res = Vector2(0, 0)
        if isinstance(other, Vector2):
            res.set_x(self.get_x() / other.get_x())
            res.set_y(self.get_y() / other.get_y())
        else:
            res.set_x(self.get_x() / other)
            res.set_y(self.get_y() / other)
        return res

    def __eq__(self, other):
        return self.get_x() == other.get_x() and self.get_y() == other.get_y()

    def __neq__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.get_x() < other.get_x() and self.get_y() < other.get_y()

    def __le__(self, other):
        return self.get_x() <= other.get_x() and self.get_y() <= other.get_y()

    def __gt__(self, other):
        return self.get_x() > other.get_x() and self.get_y() > other.get_y()

    def __ge__(self, other):
        return self.get_x() >= other.get_x() and self.get_y() >= other.get_y()

    def __repr__(self):
        return str((self.get_x(), self.get_y()))

class Matrix2(Matrix):
    def __init__(self, *args):
        self.m = [[0, 0] for i in range(2)]
        arglen = len(args)
        if arglen == 0:
            pass
        elif arglen == 1:
            self.m = args[0]
        elif arglen == 2:
            for i in range(2):
                self.m[i] = [args[i][0], args[i][1]]
        elif arglen == 4:
            self.m = [[args[0], args[1]], [args[2], args[3]]]
        else:
            raise Exception("invalid number of parameters")

    def __mul__(self, other):
        if isinstance(other, Vector2):
            x = self.m[0][0] * other.get_x() + self.m[0][1] * other.get_y()
            y = self.m[1][0] * other.get_x() + self.m[1][1] * other.get_y()
            return Vector2(x, y)
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
                        retm[i][j] += self[i][k] * other[k][j]
            return retm

    def __add__(self, other):
        retm = Matrix2()
        for i in range(2):
            for j in range(2):
                retm[i][j] = self[i][j] + other[i][j]
        return retm

    def __sub__(self, other):
        retm = Matrix2()
        for i in range(2):
            for j in range(2):
                retm[i][j] = self[i][j] - other[i][j]
        return retm

    def __repr__(self):
        return str(self.m)

def acos(x):
    return math.acos(min(1, max(x, -1)))

def sigmoid(x):
    if isinstance(x, int) or isinstance(x, float):
        return float(1/(1 + math.e**(-x)))
    elif isinstance(x, list):
        return [sigmoid(n) for n in x]
    elif isinstance(x, Vector):
        return Vector([sigmoid(n) for n in x])
    else:
        raise TypeError("sigmoid only accepts arguments of type int, float, list, or Vector")
