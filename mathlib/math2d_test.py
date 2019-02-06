from AML.math2d import *

v1 = Vector2(50,50)
v1r = 40
v2 = Vector2(100,100)
v2r = 50

v1v2 = v2 - v1
v2v1 = -v1v2

v1v2u = v1v2/v1v2.mag()
v2v1u = v2v1/v2v1.mag()

v1rv = v1 + v1v2u*v1r
v2rv = v2 + v2v1u*v2r

vmid = v1rv - v2rv

print(vmid)



