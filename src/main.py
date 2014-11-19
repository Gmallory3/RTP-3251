# Test class
# @author aashish9patel
# @version 0.10

from connection import Connection
from packet import Packet

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
    print ("main")
    
    inp = int(input('0:Client or 1:server = '))
    if (inp == 0):
      client()
    elif (inp == 1):
      server()
    else:
      print ("Invalid Input.")
      
      
#Server commands
    def setWindow(self, size):
      #Command:     window W (only for projects that support pipelined and bi-directional transfers)
      # W: the maximum receiver’s window-size at the FTA-Server (in segments).
      # NOTE: AVAILABLE TO BOTH CLIENT AND SERVER
      self.window = size
    
    def terminate(self):
      #Shuts down FTA-Server gracefully
      pass 
      
      
    #Client commands
    def connect(selfs):
      #Command:     connect (only for projects that support bi-directional transfers)
      #The FTA-client connects to the FTA-server (running at the same IP host). 
      pass
    def getF(self):
      #Command:     get F (only for projects that support bi-directional transfers)
      #The FTA-client downloads file F from the server (if F exists in the same directory as the fta-server executable).
      pass
    def postF(self):
      #Command:     post F (only for projects that support bi-directional transfers)
      #The FTA-client uploads file F to the server (if F exists in the same directory as the fta-client executable).
      pass
    def disconnect(self):
      #Command:     disconnect (only for projects that support bi-directional transfers)
      #The FTA-client terminates gracefully from the FTA-server. 
      pass
      
      
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
        