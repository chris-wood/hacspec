from p256 import *
from hacspec.speclib import *

a256 = to_felem(prime - 3)
b256 = to_felem(41058363725152142129326129780047268409114441015993725554835256314039467401291)

def map2p256(t:felem_t) -> affine_t:    
    alpha = -(fsqrt(t))
    frac = finv((fadd(fsqr(alpha), alpha)))
    x2 = fmul(fmul(-b256, finv(a256), fadd(1, frac)))
    
    x3 = fmul(alpha, x2)
    h2 = fadd(x2^3, fadd(fmul(a256, x2), b256))
    h3 = fadd(x3^3, fadd(fmul(a256, x3), b256))

    e = fexp(h2, ((fadd(prime, -1)) / 2))
    if e == 1:
    	return x2
    else:
    	return x3