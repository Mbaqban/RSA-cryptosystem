from primality import get_random_prime


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)
# or we can just use gcd from math library
# from math import gcd


class RSA():
    def __init__(self, bites):
        self.bites = bites

    def find_e(self, phi_n):
        for i in range(2, phi_n):
            if gcd(i, phi_n) == 1:
                return i

    def find_inverse(self, m, b):  # finde invers of (b) in Galois field (m)
        A = {1: 1, 2: 0, 3: m}
        B = {1: 0, 2: 1, 3: b}
        T = {1: 0, 2: 0, 3: 0}
        Q = 0
        while True:
            if B[3] == 0:
                return A[3]  # no inverses
            if B[3] == 1:
                return B[2]  # B2 = b^-1 mod m
            Q = A[3] // B[3]
            T[1] = (A[1] - (Q * B[1]))
            T[2] = (A[2] - (Q * B[2]))
            T[3] = (A[3] - (Q * B[3]))
            A = B.copy()
            B = T.copy()

    def make_keys(self):
        # MillerRabin test used for generate prime mumbers
        # generate prime mumbers in bites size

        # selecting two large primes at random : p,q
        p = get_random_prime(self.bites)
        q = get_random_prime(self.bites)

        # computing their system modulus : N=p.q
        # note ø(N)=(p-1)(q-1)
        N = p*q
        phi_n = (p-1)*(q-1)

        # selecting at random the encryption key e
        # where 1<e<ø(N), gcd(e,ø(N))=1
        e = self.find_e(phi_n)

        # solve following equation to find decryption key d
        # e.d=1 mod ø(N) and 0≤d≤N

        # first finde invers of e in Galois field phin_n
        d = self.find_inverse(m=phi_n, b=e)

        # make shure d is positive
        # 0≤d≤N
        while d < 0:
            d += phi_n

        # publish their public encryption key : KU={e,N}
        # keep secret private decryption key : KR={d,p,q}
        self.__keys = {
            "pub_key": {
                "e": e,
                "N": N
            },
            "pv_key": {
                "d": d,
                "p": p,
                "q": q
            }
        }

    # to encrypt a message the sender:
    #   obtains public key of recipient KU={e,N}
    #   computes: C=M**e mod N, where 0≤M<N
    def encrypt(self, message):
        N = self.__keys['pub_key']['N']
        e = self.__keys['pub_key']['e']

        if message > N:
            print(f"\nerror : message must be smaller than {N}\n")
            return None
        cypher_text = (message ** e) % N

        return cypher_text

    # to decrypt the ciphertext C the owner:
    #   uses their private key KR={d,p,q}
    #   computes: M=C**d mod N
    def decrypt(self, cypher_text):
        d = self.__keys['pv_key']['d']
        N = self.__keys['pub_key']['N']

        message = (cypher_text ** d) % N

        return message


A = RSA(bites=10)
A.make_keys()

print(A.decrypt(A.encrypt(595758)))
