# Manage packet
# @author aashish9patel, gmallory
# @version 0.5

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
        self.acknowledgmentNumbers = [1233]
        self.outgoingBFR = []
        self.applicationBFR = []
        self.tmpIncomingBFR = []
        self.BUFFER_SIZE = self.window * 1024
        self.publicKey, self.privateKey = self.RSA()

    """
    Packetize the data and add to outgoing buffer
    1. Handles seq & ack number wrapping around
    2. Handles the checksum & encryption
    """
    def addOutgoing(self, ctrlBits=0x0, data=""):
      # set default values for checksum
      seqNum = self.sequenceNumber
      #increment sequence number until you need to wrap around to 0
      if (self.sequenceNumber < 2**16-1):
        self.sequenceNumber += 1
      else:
        seqNum = 0
        self.sequenceNumber = 0
      
      data = self.encrypt(data, self.publicKey)
      #print data
      pkt = Packet(self.sourcePort, self.destinationPort, seqNum, 0, self.window, None, ctrlBits, data)
      pkt.checksum = self.checksum(pkt)
 
      self.outgoingBFR.append((self.packetToString(pkt), -1, 0))
    
    def addOutgoingFile(self, dataIn):
      for i in range(0, int(math.ceil(float(len(dataIn))/(self.BUFFER_SIZE/self.window)))):
        if(int(math.ceil(float(len(dataIn))/(self.BUFFER_SIZE/self.window))) == 1):
          self.addOutgoing(data=dataIn,ctrlBits=0x1)
          self.addOutgoing(ctrlBits=0x1)
        else:
          if(i == 0):
            self.addOutgoing(data=dataIn[0:(self.BUFFER_SIZE/self.window)], ctrlBits=0x1)
          elif (i == int(math.ceil(float(len(dataIn))/(self.BUFFER_SIZE/self.window)))-1):
            self.addOutgoing(data=dataIn[i*(self.BUFFER_SIZE/self.window):], ctrlBits=0x1)
          else:
            self.addOutgoing(data=dataIn[(i*self.BUFFER_SIZE/self.window):(i+1)*(self.BUFFER_SIZE/self.window)])
    
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
          
      if (pkt.checksum == self.checksum(pkt)):
        pkt.data = self.decrypt(pkt.data, self.privateKey)
        #print pkt.data
        return pkt
      else: 
        pkt.ctrlBits = 0xF
        return pkt
    
    """
    Either adds information to application buffer or recognizes packet as acknowledgment packet and eliminates corresponding sequence packet
    """
    def addIncoming(self, hexString):
      packet = self.stringToPacket(hexString)
      if packet.ctrlBits != 0xF: # Check validity
        #handshake ctrl flags
        if (packet.ctrlBits == 0xC or packet.ctrlBits == 0x4):
          return
        #ack
        elif packet.ctrlBits == 0x8:
          #handshake reminants
          if(packet.acknowledgmentNumber == 0x0):
            for n,i in enumerate(self.outgoingBFR):
              if self.stringToPacket(i[0]).ctrlBits == 0xC:
                self.outgoingBFR.pop(n)
                break
            return
          #remove from outgoingBFR
          remove = []
          for n,i in enumerate(self.outgoingBFR):
            if(self.stringToPacket(i[0]).sequenceNumber == packet.acknowledgmentNumber):
              remove.append(n)
          remove.reverse()
          for i in remove:
            self.outgoingBFR.pop(i)
          del remove[:]
        else:
          #Deal with data
          # discard duplicates
          found = False
          for i in self.tmpIncomingBFR:
            if i[0] == packet.sequenceNumber:
              found = True
          
          if(packet.sequenceNumber < self.acknowledgmentNumbers[0]):
            found = True
          elif(packet.sequenceNumber in self.acknowledgmentNumbers):
            found = True
          else:
            self.acknowledgmentNumbers.append(packet.sequenceNumber)
            self.acknowledgmentNumbers.sort()
            if(len(self.acknowledgmentNumbers) > 1):
              while((len(self.acknowledgmentNumbers) > 1) and (self.acknowledgmentNumbers[1]-self.acknowledgmentNumbers[0] == 1)):
                self.acknowledgmentNumbers.pop(0)

          if(not found):
            self.tmpIncomingBFR.append((packet.sequenceNumber, packet.data, packet.ctrlBits))

          c_idx = []
          for i in self.tmpIncomingBFR:
            if i[2] == 0x1: c_idx.append(i[0])
          if(len(c_idx) == 2):
            c_idx.sort()
            tmpArr = [None]*(c_idx[1] - c_idx[0] + 1)
            remove = []
            for n,i in enumerate(self.tmpIncomingBFR):
              if((i[0] >= c_idx[0]) and (i[0] <= c_idx[1])):
                tmpArr[i[0]-c_idx[0]] = i[1]
                remove.append(n)
            if(len(remove) == (c_idx[1]-c_idx[0]+1)):
              self.applicationBFR.append(''.join(tmpArr))
              remove.reverse()
              for i in remove:
                self.tmpIncomingBFR.pop(i)
            del remove[:]
            del tmpArr[:]

          #Generate ACK packet
          seqNum = self.sequenceNumber
          #increment sequence number until you need to wrap around to 0
          if (self.sequenceNumber < 2**16-1):
            self.sequenceNumber += 1
          else:
            seqNum = 0
            self.sequenceNumber = 0
          ackNum = packet.sequenceNumber
          for i in self.outgoingBFR:
            if(self.stringToPacket(i[0]).acknowledgmentNumber == ackNum):
              return

          pkt = Packet(self.sourcePort, self.destinationPort, seqNum, ackNum, self.window, None, 0x8, '')
          pkt.checksum = self.checksum(pkt)
          
          self.outgoingBFR.append((self.packetToString(pkt), -1, 0))

    
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
        # 1: Calculate 2 large, random primes
        while True:
            p = random.randrange(1000000, 999999999, 2)
            if all(p % n != 0 for n in range(3, int((math.sqrt(p)) + 1), 2)):
                p = 61
                break
        while True:
            q = random.randrange(1000000, 999999999, 2)
            if all(q % n != 0 for n in range(3, int((math.sqrt(q)) + 1), 2)):
                q = 53
                break
        
        # 2: Compute n = p*q
        n = p*q
        
        # 3: Compute Euler's totient function =  n -(p + q -1)
        euler = (p-1)*(q-1)
        # print (p,q,n,euler)
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
        # print ("n: " + str(n))
        # print ("euler: " + str(euler))
        # print ("e: " + str(e))
        # print ("d: " + str(d))
        
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
