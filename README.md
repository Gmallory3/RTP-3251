RTP-3251
========

Networking protocol


Test commmit from host


Notes on checksum:
"""
      BELOW is place holder code to enable us to move forward with a checksum. 
      It is necessary to come back and code this ourselves for full credit for checksum
      https://docs.python.org/2/library/hashlib.html
      
      hashableMaterial = str(packet.sourcePort) + str(packet.destinationPort) + str(packet.sequenceNumber)\
        + str(packet.acknowledgmentNumber) + str(packet.window) + str(packet.ctrlBits) + str(packet.data)
      
      sum = hashlib.md5()
      sum.update(hashableMaterial)
      sum.digest()
      print ("sum:")
      print (sum)
      print ("digest")
      print (sum.digest)
      print ("m digest size: ")
      print (sum.digest_size)
      print ("m block size: ")
      #print ( sum.blocksize)
      self.checksum = sum
      return sum
      """
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

            
  """   
  API COMMANDS:
  
      FTA SERVER
Command-line:   fta-server X A P
The command-line arguments are: 
X: the port number at which the fta-server’s UDP socket should bind to (odd number)
A: the IP address of NetEmu
P: the UDP port number of NetEmu

      FTA CLIENT
Command-line:   fta-client X A P
The command-line arguments are:
X: the port number at which the fta-client’s UDP socket should bind to (even number). Please remember that this port number should be equal to the server’s port number minus 1.
A: the IP address of NetEmu
P: the UDP port number of NetEmu

  """