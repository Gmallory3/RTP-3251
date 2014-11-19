'''
Created on Nov 19, 2014

@author: Garrett
'''

class Packet():
    
    def __init__(self, sourcePort, destinationPort, sequenceNumber, acknowledgmentNumber, 
                 window, checksum, ctrlBits, offset, options, padding, data):
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.sequenceNumber = sequenceNumber
        self.acknowledgmentNumber = acknowledgmentNumber
        self.window = window
        self.checksum = checksum
        self.ctrlBits = ctrlBits
        self.offset = offset
        self.options = options
        self.padding = padding
        self.data = data

class PacketManager():
    def __init__(self, sourcePort, destinationPort, sequenceNumber=-1, acknowledgmentNumber=-1, 
                 window=10, ctrlBits=0x0, options=None, data=None):
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.window = window
        self.ctrlBits = ctrlBits
        self.options = options
        self.data = data
        # TODO these needs to happen automatically based on data
        if(sequenceNumber == -1)
            #TODO
            print "YO DAWG FIX ME"
        else 
            self.sequenceNumber = sequenceNumber #this should be either automatic (smarter than default 0) or set by param
        if(acknowlgmentNumber == -1)
            #TODO
            print "YO DAWG FIX ME TOO"
        else
            self.acknowlgmentNumber = acknowledgmentNumber #this should be either automatic (smarter than default 0) or set by param
        
        self.checksum = checksum
        self.offset = offset
        self.padding = padding 

        def encrypt(self, message):
        publicKey = self.RSA()
        return message**publicKey[1]%publicKey[0]
            
        def decrypt(self, privateKey):
            return privateKey[1]%privateKey[0]
                
        """
        RSA algorithm used for encryption.
        https://en.wikipedia.org/wiki/RSA_(cryptosystem)
        """
        def RSA(self):
            #allows for seeding RSA with known values for testing if values supplied.
            if (_DEBUG == True):
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
            
            # 4: Chose integer e such that 1 < e < euler & gcd (e, euler)) = 1
            while True:
                e = random.randrange(1, euler, 2)
                if all(e % n != 0 for n in range(3, int((math.sqrt(e) + 1), 2))):
                    # e is prime. now if e is not divisor of 3120, we're good.
                    if (euler%e == 0):
                        break
            
            # 5: Determine d =- e^-1 mod(euler) (I.e. solve d * e =- 1(mod(euler))
            d = self.modinv(e, euler)
            
            publicKey = (n, e)
            privateKey = (n, d)
            if (_DEBUG == True):
                print ("n: " + n)
                print ("euler: " + euler)
                print ("e: " + e)
                print ("d: " + d)
            return publicKey
        
        #####
        """
        NOTE: THE FOLLOWING TWO METHODS (egcd, modinv) ARE FROM https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
        AND ARE SUBJECT TO REVIEW
        """
        ####
        def egcd(self, a, b):
            if a == 0:
                return (b, 0, 1)
            else:
                g, y, x = self.egcd(b % a, a)
                return (g, x - (b // a) * y, y)

        def modinv(self, a, m):
            g, x, y = self.egcd(a, m)
            if g != 1:
                raise Exception('modular inverse does not exist')
            else:
                return x % m