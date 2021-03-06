# Manage serverApplication
# @author gmallory, aashish9patel
# @version 1.00

import os
from connection import Connection
try:
   import cPickle as pickle
except:
   import pickle


class ServerApplication():
    '''  
    Used for testing the methods that will be available via the RTP-3251 API
    '''

    def __init__(self, _debug=False):
      self._debug = _debug
      pass
    
    def openServer(self, portOfServer=12001):
      self.serverConnection = Connection(self._debug)
      self.serverConnection.open(portOfServer)
    
    def listen(self):
      while(1):
        serialObj = None
        while(serialObj == None):
          serialObj = self.serverConnection.receive() #stuck until receives a file read or write request

        requestObj = pickle.loads(serialObj)
        if (requestObj[0] == "FFFFFFFF"): #client wants file
          self.replyF(requestObj[1])
        else: #client is posting file as ['filename', content]
          f = open(requestObj[0],'w')
          f.write(requestObj[1])
          f.close()
          fileConfirmation = [requestObj[0], 'confirmed']
          self.serverConnection.send(pickle.dumps(fileConfirmation))
      
    def replyF(self, fileName):
      #Command:     post F (only for projects that support bi-directional transfers)
      #The FTA-client uploads file F to the server (if F exists in the same directory as the fta-client executable).
      f = open(fileName, 'r')
      obj = [fileName+"FromServer", f.read()]
      f.close()
      self.serverConnection.send(pickle.dumps(obj))
      
    
    def terminate(self):
      #Shuts down FTA-Server gracefully
      self.serverConnection.terminate()
        
if __name__ == "__main__":
  serverApp = ServerApplication(_debug=True)
  print ('Server application started')
  serverApp.openServer()
  print ('Connection opened')
  serverApp.listen()
