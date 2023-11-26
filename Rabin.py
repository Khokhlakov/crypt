#source: https://asecuritysite.com/encryption/rabin2

import random
from Crypto.Util.number import *
import codecs
import Crypto
from Crypto import Random

def encryption(plaintext, n):
    # c = m^2 mod n
    
    plaintext = padding(plaintext)
    
    if plaintext >= n: print("ERROR: too long plain text")
    return (plaintext ** 2) % n

def simpleEncryption(msg, n):
    plaintext =  bytes_to_long(msg.encode('utf-8'))
    # c = m^2 mod n
    plaintext = padding(plaintext)
    if plaintext >= n: print("ERROR: too long plain text")
    return (plaintext ** 2) % n


def padding(plaintext):
    binary_str = bin(plaintext)     # convert to a bit string
    output = binary_str + binary_str[-16:]      # pad the last 16 bits to the end
    return int(output, 2)       # convert back to integer

def decryption(a, p, q):
    n = p * q
    r, s = 0, 0
    # find sqrt
    # for p
    if p % 4 == 3:
        r = sqrt_p_3_mod_4(a, p)
    elif p % 8 == 5:
        r = sqrt_p_5_mod_8(a, p)
    # for q
    if q % 4 == 3:
        s = sqrt_p_3_mod_4(a, q)
    elif q % 8 == 5:
        s = sqrt_p_5_mod_8(a, q)

    gcd, c, d = egcd(p, q)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]
    #print (lst)
    plaintext = choose(lst)

    string = bin(plaintext)
    string = string[:-16]
    plaintext = int(string, 2)

    return plaintext


# decide which answer to choose
def choose(lst):

    for i in lst:
        binary = bin(i)

        append = binary[-16:]   # take the last 16 bits
        binary = binary[:-16]   # remove the last 16 bits

        if append == binary[-16:]:
            return i
    return

# Find SQROOT in Zp where p = 3 mod 4
def sqrt_p_3_mod_4(a, p):
    r = pow(a, (p + 1) // 4, p)
    return r


# Find SQROOT in Zp where p = 5 mod 8
def sqrt_p_5_mod_8(a, p):
    d = pow(a, (p - 1) // 4, p)
    r =0
    if d == 1:
        r = pow(a, (p + 3) // 8, p)
    elif d == p - 1:
        r = 2 * a * pow(4 * a, (p - 5) // 8, p) % p

    return r

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, y, x = egcd(b % a, a)
        return gcd, x - (b // a) * y, y



#Funciones extras añadidas para usar en la interfaz

#bits (tamaño de la clave publica) debe ser par, preferiblemente: 2048, 1024, 512
def generate_keys_rabin(bits = 2048):
    while True:
            p = Crypto.Util.number.getPrime(bits//2, randfunc=Crypto.Random.get_random_bytes)
            if ((p % 4)==3): break

    while True:
            q = Crypto.Util.number.getPrime(bits//2, randfunc=Crypto.Random.get_random_bytes)
            if ((q % 4)==3): break
    n = p*q
    return n, p, q

def encrypt_rabin(msg, n = None):
    if n is None: 
          n,p,q = generate_keys_rabin(bits = 2048)
    
    plaintext =  bytes_to_long(msg.encode('utf-8'))
    return encryption(plaintext, n), n, p, q

def decrypt_rabin(ciphertext, p, q):
    plaintext = decryption(ciphertext, p, q)
    st=format(plaintext, 'x')
    return bytes.fromhex(st).decode()

def new_test():
    #mensaje a cifrar
    msg="hello, my name is Earl123\##$%#$&/$/%$%/$/()/=?¡1231ñ3"
    #encrypt(msg,n) te entrega el mensaje cifrado, la clave publica n, y las claves privadas p y q. 
    #n es opcional, si no lo das, se generará una clave aleatoria
    ciphertext, n, p, q = encrypt_rabin(msg)
    print("ciphertext: ", ciphertext)
    #para desencriptar es necesario dar un mensaje cifrado, y la clave privada p y q
    deciphered_text = decrypt_rabin(ciphertext, p, q)
    print("n: ",n)
    print("p: ", p)
    print("q: ",q)
    print("deciphered text: ", deciphered_text)


#new_test()