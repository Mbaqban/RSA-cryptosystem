# RSA-cryptosystem

implementation of rsa algorithm in python

## Installation

its script dont need installation

## Usage

```python
rsa_system = RSA(bites=10)
rsa_system.make_keys()
char = "a"
char_to_int = ord(char)

c = rsa_system.encrypt(message=char_to_int)

m = rsa_system.decrypt(cypher_text=c)

print(chr(m))
```

bites is size of prime numbers that algorithm use.
posetive integer number   4 <= bites <= 10

