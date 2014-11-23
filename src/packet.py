'''
Created on Nov 19, 2014

@author: Garrett
'''

import hashlib
import math
import random

class Packet():
    
    def __init__(self, sourcePort, destinationPort, sequenceNumber, acknowledgmentNumber, 
                 window, checksum, ctrlBits, data):
        #int: sourcePort,destPort, sequence, ackNum, window, checksum 
        #hex: ctrlbits
        #str: data 
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.sequenceNumber = sequenceNumber
        self.acknowledgmentNumber = acknowledgmentNumber
        self.window = window
        self.checksum = checksum
        self.ctrlBits = ctrlBits
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
        
        self.sequenceNumber = 1234
        self.acknowledgeNumber = 5678
        self.outgoingBFR = []
        #self.incomingBFR = []
        self.applicationBRF = []
        self.publicKey, self.privateKey = self.RSA()
        
                
    """
    Packetize the data and add to outgoing buffer
    1. Handles seq & ack number wrapping around
    2. Handles the checksum & encryption
    """
    def addOutgoing(self, ctrlBits=0x0, data=""):
      # set default values for checksum
      
      seqNum = self.sequenceNumber
      ackNum = self.acknowledgeNumber
      #increment sequence number until you need to wrap around to 0
      if (data == "" and self.sequenceNumber < 2**16):
        self.sequenceNumber += 1
      elif(data == "" and self.sequenceNumber >= 2**16):
        seqNum = 0
        self.sequenceNumber = 0
        
      #increment ack numbers until you need to wrap -- access this only in data is EMPTY
      elif(data != "" and self.acknowledgeNumber < 2**16):
        self.acknowledgeNumber += 1
      elif(data != "" and self.acknowledgeNumber >= 2**16):
        ackNum = 0
        self.acknowledgeNumber = 0
      
      #data = self.encrypt(data, self.publicKey)
      pkt = Packet(self.sourcePort, self.destinationPort, seqNum, ackNum, self.window,
                   None, ctrlBits, data)
      pkt.checksum = self.checksum(pkt)
      """
      print("src port: " + str(pkt.sourcePort))
      print("dest port: " + str(pkt.destinationPort))
      print("seq num: " + str(pkt.sequenceNumber))
      print("ack num: "+ str(pkt.acknowledgmentNumber))
      print("window: " + str(pkt.window))
      print("chk sum: "+ str(pkt.checksum))
      print("ctrl bits: " + str(pkt.ctrlBits))
      print("data: " + str(pkt.data))
      """
      
      self.outgoingBFR.append((self.packetToString(pkt), -1, 0))
    
    """
    Changes a packet object to a hex string of the format '######...' and length 40 + data
    1. Does NOT include a '0x' at the beginning
    2. return string
    """
    def packetToString(self, packet):
      return (4-len(hex(packet.sourcePort)[2:]))*'0' + hex(packet.sourcePort)[2:] \
        + (4-len(hex(packet.destinationPort)[2:]))*'0' + hex(packet.destinationPort)[2:]\
        + (8-len(hex(packet.sequenceNumber)[2:]))*'0' + hex(packet.sequenceNumber)[2:]\
        + (8-len(hex(packet.acknowledgmentNumber)[2:]))*'0' + hex(packet.acknowledgmentNumber)[2:]\
        + (4-len(hex(packet.window)[2:]))*'0' + hex(packet.window)[2:]\
        + (4-len(hex(packet.checksum)[2:]))*'0' + hex(packet.checksum)[2:]\
        + hex(packet.ctrlBits)[2:]\
        + 7*'0'\
        + packet.data.encode("hex")
      
    """
    Iterates through a hex string of format '#######...' and length 40 + data
    1. return decrypted packet if it passes the checksum. Check sum operates on encrypted data field
    2. return ctrlBits = 0xF if it FAILS checksum
    """  
    def stringToPacket(self, hexString):
      sourcePort = int(hexString[0:4], 16)
      destinationPort = int(hexString[4:8], 16)
      sequenceNumber = int(hexString[8:16], 16)
      acknowledgmentNumber = int(hexString[16:24], 16)
      window = int(hexString[24:28], 16)
      checksum = int(hexString[28:32], 16)
      ctrlBits = int(hexString[32], 16)
      data = hexString[40:].decode("hex")
    
      pkt = Packet(sourcePort, destinationPort, sequenceNumber, acknowledgmentNumber, 
                 window, checksum, ctrlBits, data)
      
      """
      print("src port: " + str(pkt.sourcePort))
      print("dest port: " + str(pkt.destinationPort))
      print("seq num: " + str(pkt.sequenceNumber))
      print("ack num: "+ str(pkt.acknowledgmentNumber))
      print("window: " + str(pkt.window))
      print("chk sum: "+ str(pkt.checksum))
      print("ctrl bits: " + str(pkt.ctrlBits))
      print("data: " + str(pkt.data))
      """
      
      if (pkt.checksum == self.checksum(pkt)):
        #pkt.data = self.decrypt(pkt.data, self.privateKey)
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
        self.applicationBRF.append(packet.data)
    
    
    """
    16-bit Fletcher's Checksum. Returns a int value 0-65535 (i.e. 16 bit int)
    """
    def checksum(self, packet):
      """
      https://en.wikipedia.org/wiki/Fletcher%27s_checksum
      As described in the article above:
      Step 1: divide up binary word (i.e. hashable material) into 8 bit blocks
      1b: if string of characters, each string is an 8 bit btye
      
      Step 2: Add up all 8 bit blocks of message
      Step 3: mod the result by 255 (can be taken at every step to keep size down)
      Step 4: Keep a running sum of the values computed in step 3, moding it by 255 as well
      Step 5: combine the running sum and the simple sum into a 16 bit checksum
      """
      hashableMaterial = str(packet.sourcePort) + str(packet.destinationPort) + str(packet.sequenceNumber)\
        + str(packet.acknowledgmentNumber) + str(packet.window) + str(packet.ctrlBits) + packet.data
      
      sum1 = 0
      sum2 = 0
      for block in hashableMaterial:
        sum1 = (sum1 + ord(block)) % 255
        sum2 = (sum2 + sum1) % 255
      
      fletchersSum = sum1 + sum2*256
      return fletchersSum

    """
    Encryption by RSA. 
    1. message comes in as string
    2. ascii of each string character is number that is encrypted.
    3. keep a string record of all encrypted characters
    3. hex of string is taken and put into packet ->> this step occurs in addOutgoing()
    """
    def encrypt(self, message, publicKey):
        cipherText = ''
        for letter in message:
            number = ord(letter)**publicKey[1]%publicKey[0]
            cipherText += str(number) + ','
                    
        return cipherText
    
    """
    De-encryption by RSA.
    1. hex taken out and made into string ->> occurs in addIncoming()
    2. parse string on ',' character to separate out each encrypted number
    2. convert each number into original letter
    """   
    def decrypt(self, cipherText, privateKey):
        plainText = ''
        for letter in cipherText.split(','):
            if(letter != ''): #needed because the cipherText ends with a ',' so it appends an empty string to the end of split
                plainText +=  chr(int(letter)**privateKey[1]%privateKey[0])
        return plainText
                
    """
    RSA algorithm used for encryption.
    https://en.wikipedia.org/wiki/RSA_(cryptosystem)
    """
    def RSA(self):
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
        print (p,q,n,euler)
        # 4: Chose integer e such that 1 < e < euler & gcd (e, euler)) = 1
        while True:
          e = 17
          break
          e = random.randrange(1, euler, 2)
          if all(e % n != 0 for n in range(3, int(math.sqrt(e)) + 1, 2 )):
            # e is prime. now if e is not divisor of 3120, we're good.
            if (euler%e == 0):
              break
          
        
        # 5: Determine d =- e^-1 mod(euler) (I.e. solve d * e =- 1(mod(euler))
        d = self.modinv(e, euler)
        
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