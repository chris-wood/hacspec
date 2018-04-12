from curve25519 import *
from speclib import *
from sha2 import sha256

a25519 = felem(486662)
b25519 = felem(1)
u25519 = felem(2)

def f_25519(x:felem_t) -> felem_t:
    return fadd(fmul(x,fsqr(x)),fadd(fmul(a25519,fsqr(x)),x))
        
# def hash2curve25519(alpha:vlbytes) -> point_t :
    # r = felem(bytes.to_nat_be(sha256(alpha)))

def hash2curve25519(r:felem_t) -> point_t :
    d = felem(p25519 - fmul(a25519,finv(fadd(1,fmul(u25519,fsqr(r))))))
    power = nat((p25519 - 1)//2)
    e = fexp(f_25519(d), power)
    if e != 1:
        return fsub(-d,a25519) # -d - (1 - -1)A/u = -d - (-2)A/2 = -d -- A = -d + A
    else:
        return d

alphas = [1, 7, 13, 1<<7, 1<<8, 1<<64, 1<<64-1, p25519-1, p25519+1]
for alpha in alphas:
	print(hash2curve25519(felem(alpha)))