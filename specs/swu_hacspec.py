from p256 import *
from hacspec.speclib import *

a256 = prime - 3
b256 = 41058363725152142129326129780047268409114441015993725554835256314039467401291

def f_p256(x:felem_t) -> felem_t:
    return fadd(fexp(x, 3), fadd(fmul(to_felem(a256), x), to_felem(b256)))

def x1(t:felem_t, u:felem_t) -> felem_t:
    return u

def x2(t:felem_t, u:felem_t) -> felem_t:
    coefficient = fmul(to_felem(-b256), finv(to_felem(a256)))
    t4 = fexp(t, 4)
    gu2 = fsqr(f_p256(u))
    denom = fadd(gu2, fmul(fsqr(t), f_p256(u)))
    denom = fmul(t4, denom)
    return fmul(coefficient, fadd(to_felem(1), finv(denom)))

def x3(t:felem_t, u:felem_t) -> felem_t:
    return fmul(fsqr(t), fmul(f_p256(u), x2(t, u)))

def U(t:felem_t, u:felem_t) -> felem_t:
    return fmul(fexp(t, 3), fmul(fsqr(f_p256(u)), f_p256(x2(t, u))))

def map2p256(t:felem_t) -> affine_t:
    u = fadd(t, to_felem(1))
    x1v = x1(t, u)
    x2v = x2(t, u)
    x3v = x3(t, u)
    Utu = fsqr(U(t, u))

    exp = (fadd(to_felem(prime), to_felem(-1))) // to_felem(2)
    e1 = fexp(f_p256(x1v), exp)
    e2 = fexp(f_p256(x2v), exp)

    exp = (fadd(to_felem(prime), to_felem(1))) // to_felem(4)
    if e1 == 1:
        return (x1v, fexp(f_p256(x1v), exp))
    elif e2 == 1:
        return (x2v, fexp(f_p256(x2v), exp))
    else:
        return (x3v, fexp(f_p256(x3v), exp))

inputs = [1, 7, 13, 1<<7, 1<<8, 1<<64, 1<<64-1, prime-1, prime+1]
for u in inputs:
    print(u, map2p256(to_felem(u)))