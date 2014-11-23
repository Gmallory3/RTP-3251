'''
Created on Nov 19, 2014

@author: Garrett
'''

class Packet():
    
    def __init__(self, sourcePort, destinationPort, sequenceNumber, acknowledgmentNumber, 
                 window, checksum, ctrlBits, padding, data):
        #int: sourcePort,destPort, sequence, ackNum, window
        #hex: checksum, ctrlbits, padding
        #str: data 
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.sequenceNumber = sequenceNumber
        self.acknowledgmentNumber = acknowledgmentNumber
        self.window = window
        self.checksum = checksum
        self.ctrlBits = ctrlBits
        self.padding = padding
        self.data = data


class PacketManager():
  
    """
    Sets up a Packet Manager for one connection. 
    1. SourcePort and destinationPort are connection specific and are set with parameters
    2. Window defaults to 10. Any changes should come from directly referencing the variable in connection.py
    3. Creates a public and private key with RSA
    """
    def __init__(self, sourcePort, destinationPort):
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.window = 10
        
        self.sequenceNumber = 0
        self.acknowledgeNumber = 0
        self.outgoingBFR = []
        #self.incomingBFR = []
        self.applicationBRF = []
        #self.publicKey, self.privateKey = self.RSA()
        
                
    """
    Packetize the data and add to outgoing buffer
    1. Handles seq & ack number wrapping around
    2. Handles the checksum & encryption
    """
    def addOutgoing(self, ctrlBits=0x0, data=""):
      # set default values for checksum,  padding
      
      #increment sequence number until you need to wrap around to 0
      if (data == "" and self.sequenceNumber < 2**16):
        seqNum = self.sequenceNumber
        self.sequenceNumber += 1
      elif(data == "" and self.sequenceNumber >= 2**16):
        seqNum = 0
        self.sequenceNumber = 0
      #increment ack numbers until you need to wrap -- access this only in data is EMPTY
      elif(data != "" and self.acknowledgeNumber < 2**16):
        ackNum = self.acknowledgeNumber
        self.acknowledgeNumber += 1
      elif(data != "" and self.acknowledgeNumber >= 2**16):
        ackNum = 0
        self.acknowledgeNumber = 0
      
      #encryptedData = self.encrypt(data)
      pkt = Packet(self.sourcePort, self.destinationPort, seqNum, ackNum, window,
                   None, ctrlBits, 0x000, data)
      
      checksum = self.checksum(pkt)
      pkt.checksum = checksum
      
      outgoingBFR.add((self.packetToString(pkt), -1, 0))
    
    """
    Changes a packet object to a hex string of the format '######...' and length 40 + data
    1. Does NOT include a '0x' at the beginning
    2. return string
    """
    def packetToString(self, packet):
      return hex(packet.sourcePort)[2:] + hex(packet.destinationPort)[2:] + hex(packet.acknowledgmentNumber)\
        + hex(packet.window)[2:] + str(packet.checksum) + str(packet.ctrlBits) + str(packet.padding) + packet.data.encode("hex")
      
    """
    Iterates through a hex string of format '#######...' and length 40 + data
    1. return decrypted packet if it passes the checksum. Check sum operates on encrypted data field
    2. return ctrlBits = 0xF if it FAILS checksum
    """  
    def stringToPacket(self, hexString):
      sourcePort = int(hexString[0,4])
      destinationPort = int(hexString[4,8])
      sequenceNumber = int(hexString[8,16])
      acknowledgmentNumber = int(hexString[16,24])
      window = int(hexString[24,28])
      checksum = hexString[28,32]
      ctrlBits = hexString[32]
      padding = hexString[33, 40]
      data = str(hexString[40:])
    
      pkt = Packet(sourcePort, destinationPort, sequenceNumber, acknowledgmentNumber, 
                 window, checksum, ctrlBits, padding, data)
      
      if (pkt.checksum == checksum(pkt)):
        #pkt.data = self.decrypt(pkt.data))
        return pkt
      else: 
        pkt.ctrlBits = 0xF
        return pkt
    
    """
    Either adds information to application buffer or recognizes packet as acknowledgment packet and eliminates corresponding sequence packet
    """
    def addIncoming(self, hexString):
      packet = self.stringToPacket(hexString)
      if packet.ctrlBits == 0xF: # Check validity
        return
      
      if packet.data == "": #ack pack
        indexCount = 0
        for pkt,time,count in self.outgoingBFR:# match the ack number and sequence number and remove packet from outgoing buffer if match
          outGoingPacket = self.stringToPacket(pkt)
          if (packet.acknowledgmentNumber == outGoingPacket.sequenceNumber):
            self.outgoingBFR.remove(indexCount)
          indexCount += 1
          
      else: #data pack        
        self.applicationBRF.add(packet.data)
    
    
    

    def checksum(self, packet):
      """
      BELOW is place holder code to enable us to move forward with a checksum. 
      It is necessary to come back and code this ourselves for full credit for checksum
      https://docs.python.org/2/library/hashlib.html
      """
      hashableMaterial = str(packet.sourcePort) + str(packet.destinationPort) + str(packet.sequenceNumber)\
        + str(packet.acknowledgmentNumber) + str(packet.window) + str(packet.ctrlBits) + str(packet.padding) + str(packet.data)
      
      sum = hashlib.md5()
      sum.update(hashableMaterial)
      sum.digest()
      print ("m: " + sum)
      print ("m digest: " + sum.digest)
      print ("m digest size: " + sum.digest_size)
      print ("m block size: " + sum.blocksize)
      self.checksum = sum
      """
      >>> 
      >>> m = hashlib.md5()
      >>> m.update("Nobody inspects")
      >>> m.update(" the spammish repetition")
      >>> m.digest()
      '\xbbd\x9c\x83\xdd\x1e\xa5\xc9\xd9\xde\xc9\xa1\x8d\xf0\xff\xe9'
      >>> m.digest_size
      16
      >>> m.block_size
      64
      """



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
        return publicKey, privateKey
    
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