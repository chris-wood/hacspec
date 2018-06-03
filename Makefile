#To run these specs in Python you need to install Python >= 3.6
PYTHON?=python3.6

SPECS=poly1305 chacha20 aead_chacha20poly1305 sha2 keccak \
curve25519 ed25519 p256 curve448 rsapss aes gf128 aead_aes128gcm blake2 wots kyber
OTHER_SPECS=vrf argon2i # currently broken

.PHONY: test $(SPECS) all

all: run check test

run: $(SPECS)
test: $(addsuffix -test, $(SPECS))
check: $(addsuffix -check, $(SPECS)) 

$(SPECS):
	PYTHONPATH=. $(PYTHON) -O tests/$@_test.py

%-check: specs/%.py
	PYTHONPATH=. $(PYTHON) lib/check.py $<
%-test: tests/%_test.py 
	PYTHONPATH=. $(PYTHON) $<
