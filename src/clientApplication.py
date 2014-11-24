'''
Created on Nov 17, 2014

@author: Garrett
'''

from connection import Connection
import cPickle

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
      pickledRequest = cPickle.dumps(fileRequestObk)
      self.clientConnection.send(pickledRequest)
      
      serialObj = self.clientConnection.receive()
      f = open(fileName, "w")
      f.write(cPickle.loads(serialObj)[0]) 
      
    def postF(self, fileName):
      #Command:     post F (only for projects that support bi-directional transfers)
      #The FTA-client uploads file F to the server (if F exists in the same directory as the fta-client executable).
      f = open(fileName, 'r')
      obj = [filename, f.read()]
      serialObj = cPickle.dumps(obj)
      self.clientConnection.send(serialObj)
      
      serialObj = self.clientConnection.receive()
      serverReply = cPickle.loads(serialObj)
      if (serverReply[0] == filename and serverReply[1] == "confirmed"):
        print (filename + " was confirmed")
      else:
        print (filename + " was not confirmed")
    
    def terminate(self):
      #Command:     disconnect (only for projects that support bi-directional transfers)
      #The FTA-client terminates gracefully from the FTA-server. 
      pass
      
      
      # add file confirmation
if __name__ == "__main__":
  cApp = ClientApplication()
  cApp.connect()


  
        