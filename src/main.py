# Test class
# @author aashish9patel
# @version 0.10

from connection import Connection
from packet import Packet, PacketManager
import time

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


if __name__ == '__main__':
    inp = int(input('0:Client or 1:server = '))
    if (inp == 0):
        client()
    elif (inp == 1):
        server()
    else:
        print ("Invalid Input.")
  