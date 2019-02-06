from math2d import *

v1 = Vector([1,2])
print(v1, v1.dim)
v2 = Vector(v1)
print(v2, v2.dim)

for i in v1:
    print(i)

for i in v2:
    print(i)

v1[0] = 1

for i in v2:
    print(i)

print(v2.normalized())
