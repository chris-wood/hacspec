from specs.curve25519 import *
import json
from sys import exit

def main (x: int) -> None :
    # RFC 7539 Test Vectors
    k0 = bytes.from_hex('a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4')
    u0 = bytes.from_hex('e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c')
    expected = bytes.from_hex('c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552')
    computed = scalarmult(k0, u0)
    if not is_on_curve(u0):
        print("u0 is not on curve")
        
    if expected == computed:
        print("Curve25519 Test 0 passed.")
    else:
        print("Curve25519  0 failed:")
        print("expected:",expected)
        print("computed:",computed)

    file = open('tests/test_vectors/curve25519_test_vectors.json')
    curve25519_test_vectors = json.load(file)
        
    for i in range(len(curve25519_test_vectors)):
        s = bytes.from_hex(curve25519_test_vectors[i]['private'])
        p = bytes.from_hex(curve25519_test_vectors[i]['public'])
        expected = bytes.from_hex(curve25519_test_vectors[i]['result'])
        valid = curve25519_test_vectors[i]['valid']
        computed = scalarmult(s,p)
        if not is_on_curve(p):
            if valid:
                print("Curve25519 Test ",i+1," failed (public key is not on curve).")
            else:
                print("Curve25519 Test ",i+1," passed (public key is not on curve).")
        elif (computed == expected and valid):
            print("Curve25519 Test ",i+1," passed.")
        elif (not(computed == expected) and not valid):
            print("Curve25519 Test ",i+1," passed.")
        else:
            print("Curve25519 Test ",i+1," failed:")
            print("expected mac:",expected)
            print("computed mac:",computed)
            exit(1)

main(0)
