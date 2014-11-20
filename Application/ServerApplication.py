'''
Created on Nov 17, 2014

@author: Garrett
'''

import main


class ServerApplication(object):
    '''  
    Used for testing the methods that will be available via the RTP-3251 API
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
    def connectAsClient(self, portOfClient=12000, destIp="143.215.129.100", destPort=7000):
      main.client(portOfClient, destIp, destPort)
      
    def listenAsServer(self, portOfServer=12000, destIp="143.215.129.100", destPort=7000):
      main.server(portOfServer, destIp, destPort)
    
    #Server commands
    """ eliminate"""
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
        