'''
Created on Nov 17, 2014

@author: Garrett
'''

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

    def __init__(self):
      pass
      
    #Client commands
    def connect(self, portOfClient=12000, destIp="143.215.129.100", destPort=7000):
      #Command:     connect (only for projects that support bi-directional transfers)
      #The FTA-client connects to the FTA-server (running at the same IP host). 
      self.clientConnection = Connection()
      self.clientConnection.open(portOfClient, (destIp, destPort))
    
    def getF(self, fileName):
      #Command:     get F (only for projects that support bi-directional transfers)
      #The FTA-client downloads file F from the server (if F exists in the same directory as the fta-server executable).
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
      
    def postF(self, fileName):
      #Command:     post F (only for projects that support bi-directional transfers)
      #The FTA-client uploads file F to the server (if F exists in the same directory as the fta-client executable).
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
    
    def terminate(self):
      #Command:     disconnect (only for projects that support bi-directional transfers)
      #The FTA-client terminates gracefully from the FTA-server. 
      self.clientConnection.terminate()
      
      
      # add file confirmation
if __name__ == "__main__":
  cApp = ClientApplication()
  #cApp.connect(12000, '127.0.0.1', 12001)
  cApp.connect(destIp="127.0.0.1")
  cApp.postF('file1')
  cApp.getF('file1AtServer')
  t = time.clock()
  while (time.clock() - t < 2): pass
  cApp.terminate()

  
        