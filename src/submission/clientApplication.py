# Manage clientApplication
# @author aashish9patel, gmallory
# @version 1.00

import os
from connection import Connection

try:
   import cPickle as pickle
except:
   import pickle
import time

class ClientApplication(object):
    '''  
    Used for testing the methods that will be available via the RTP-3251 API
    '''

    def __init__(self, _debug=True):
      self._debug=_debug
      
    #Command:     connect (only for projects that support bi-directional transfers)
    #The FTA-client connects to the FTA-server (running at the same IP host). 
    def connect(self, portOfClient=12000, destIp="143.215.129.100", destPort=7000):
      self.clientConnection = Connection(self._debug)
      self.clientConnection.open(portOfClient, (destIp, destPort))
    
    #Command:     get F (only for projects that support bi-directional transfers)
    #The FTA-client downloads file F from the server (if F exists in the same directory as the fta-server executable).
    def getF(self, fileName):
      fileRequestObj = ['FFFFFFFF', fileName]
      self.clientConnection.send(pickle.dumps(fileRequestObj))
      
      serialObj = None
      while(serialObj == None):
        serialObj = self.clientConnection.receive()
      fullfilledRequest = pickle.loads(serialObj)
      if (fullfilledRequest[0] == fileName+"FromServer"): #write the contents (i.e. the second item in the object array
        f = open(fileName+"FromServer", "w")
        f.write(fullfilledRequest[1]) 
        f.close()
        print ("Client successfully received", fileName+"FromServer")
      else:
        print ("Client received", fullfilledRequest[0], "but was expecting", fileName+"FromServer")
      
    #Command:     post F (only for projects that support bi-directional transfers)
    #The FTA-client uploads file F to the server (if F exists in the same directory as the fta-client executable).
    def postF(self, fileName):
      f = open(fileName, 'r')
      obj = [fileName+"AtServer", f.read()]
      f.close()
      self.clientConnection.send(pickle.dumps(obj))
      
      serialObj = None
      while(serialObj == None):
        serialObj = self.clientConnection.receive()
      
      serverReply = pickle.loads(serialObj)

      if (serverReply[0] == fileName+"AtServer" and serverReply[1] == "confirmed"):
        print (fileName + " was confirmed")
      else:
        print (fileName + " was not confirmed!")
    
    #Command:     disconnect (only for projects that support bi-directional transfers)
    #The FTA-client terminates gracefully from the FTA-server. 
    def terminate(self):
      self.clientConnection.terminate()

      
if __name__ == "__main__":
  # Creat Connection
  cApp = ClientApplication(_debug=True)
  cApp.connect(12000, "192.168.1.84", 8000)
  # Post File
  print ("Posting file")
  t = time.clock()
  cApp.postF('postFile')
  t_f = time.clock() - t
  print("Post Duration: " + str(t_f) + "s")
  print("Post Size: " + str(os.path.getsize("postFile")) + " bytes")
  # Get file
  print ("Getting file")
  t = time.clock()
  cApp.getF('serverFile')
  t_f = time.clock() - t
  print("Get Duration: " + str(t_f) + "s")
  print("Get Size: " + str(os.path.getsize("serverFile")) + " bytes")
  # terminate after two seconds
  while (time.clock() - t < 2): pass
  cApp.terminate()
