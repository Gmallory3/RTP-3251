# Test class
# @author aashish9patel
# @version 0.10

from connection import Connection
from packet import Packet, PacketManager

def client():
    clientConn = Connection()
    clientConn.open(12000, '127.0.0.1')
    while 1:
        clientConn.send(input('>>'));

def server():
    serverConn = Connection()
    serverConn.open(12001)
    serverConn.receive()


if __name__ == '__main__':
  #(self, sourcePort, destinationPort, sequenceNumber, acknowledgmentNumber,window, checksum, ctrlBits, padding, data):
  #pkt = Packet(1234, 5678, 0, 0, 10, 0x00, 0x8, "hello world")
  """
  pacman = PacketManager(1234, 5678)
  print("p k: " + str(pacman.publicKey))
  print ("hello world")
  print (pacman.encrypt("hello world",pacman.publicKey))
  """
  
  #print (pacman.checksum(pkt))
  #pacman.addOutgoing(ctrlBits= 0xF, data = "hello world")
  #print(pacman.outgoingBFR)
  
  #reversedPacket = pacman.stringToPacket(pacman.outgoingBFR[0][0])
  #print (reversedPacket)
  
  
  """
    a = [1,1,1]
    for i in a:
        i = 2
    print a
    inp = int(input('0:Client or 1:server = '))
    if (inp == 0):
        client()
    elif (inp == 1):
        server()
    else:
        print ("Invalid Input.")
  """