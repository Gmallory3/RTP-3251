# Test class
# @author aashish9patel
# @version 0.10

from connection import Connection
from packet import Packet, PacketManager
import time
import random
import math

def client():
    clientConn = Connection()
    clientConn.open(12000, ('127.0.0.1',12001))
    t = time.clock()
    while (time.clock() - t < 2): pass
    clientConn.terminate()
    # while 1:
    #     clientConn.send(input('>>'));

def server():
    serverConn = Connection()
    serverConn.open(12001)
    #serverConn.receive()

def RSA():
        #allows for seeding RSA with known values for testing if values supplied.
        if (True):
            p = 61
            q = 53
        else:
            # 1: Calculate 2 large, random primes
            while True:
                p = random.randrange(1000000, 999999999, 2)
                if all(p % n != 0 for n in range(3, int((math.sqrt(p) + 1), 2))):
                    break
            while True:
                q = random.randrange(1000000, 999999999, 2)
                if all(q % n != 0 for n in range(3, int((math.sqrt(q) + 1), 2))):
                    break
        
        # 2: Compute n = p*q
        n = p*q
        
        # 3: Compute Euler's totient function =  n -(p + q -1)
        euler = (p-1)*(q-1)
        # print (p,q,n,euler)
        # 4: Chose integer e such that 1 < e < euler & gcd (e, euler)) = 1
        while True:
#           e = 17
#           break
          e = random.randrange(1, euler, 2)
          if all(e % n != 0 for n in range(3, int(math.sqrt(e)) + 1, 2 )):
            # e is prime. now if e is not divisor of 3120, we're good.
            if (euler%e == 0):
              break
          
        
        # 5: Determine d =- e^-1 mod(euler) (I.e. solve d * e =- 1(mod(euler))
        d = modinv(e, euler)
        
        publicKey = (n, e)
        privateKey = (n, d)
        print ("n: " + str(n))
        print ("euler: " + str(euler))
        print ("e: " + str(e))
        print ("d: " + str(d))
        
        return publicKey, privateKey
    
#####
"""
NOTE: THE FOLLOWING TWO METHODS (egcd, modinv) ARE FROM https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
AND ARE SUBJECT TO REVIEW
"""
####
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

  
  
 
if __name__ == '__main__':
  #RSA()
  print (17*2753%3120)
  
   
  
#     inp = int(input('0:Client or 1:server = '))
#     if (inp == 0):
#         client()
#     elif (inp == 1):
#         server()
#     else:
#         print ("Invalid Input.")
#    