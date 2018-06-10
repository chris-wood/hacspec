from p256 import *
from hacspec.speclib import *

a256 = to_felem(prime - 3)
b256 = to_felem(41058363725152142129326129780047268409114441015993725554835256314039467401291)

def g(x:felem_t) -> felem_t:
    return fadd(fexp(x, 3), fadd(fmul(A, x), B))

def x1(t:felem_t, u:felem_t) -> felem_t:
    return u

def x2(t:felem_t, u:felem_t) -> felem_t:
    return fmul(fmul(-b256, finv(a256)), (fadd(1, (1 / (fmul(fexp(t, 4), fadd(fsqr(g(u)), fmul(t^2, g(u)))))))))

def x3(t:felem_t, u:felem_t) -> felem_t:
    return fmul(fsqr(t), fmul(g(u), x2(t, u)))

def U(t:felem_t, u:felem_t) -> felem_t:
    return fmul(fexp(t, 3), fmul(fsqr(g(u)), g(x2(t, u))))

def map2p256(t:felem_t) -> affine_t:
    u = fadd(t, 1)
    x1v = x1(t, u)
    x2v = x2(t, u)
    x3v = x3(t, u)
    Utu = fsqr(U(t, u))

    e1 = fexp(g(x1v), ((fadd(prime, -1)) / 2))
    e2 = fexp(g(x2v), ((fadd(prime, -1)) / 2))

    if e1 == 1:
        return x1v
    elif e2 == 1:
        return x2v
    else:
        return x3v