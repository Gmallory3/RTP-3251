'''
Created on Nov 17, 2014

@author: Garrett
'''

from connection import Connection
import cPickle


class ServerApplication(object):
    '''  
    Used for testing the methods that will be available via the RTP-3251 API
    '''

    def __init__(self, params):
      pass
    
    def openServer(self, portOfServer=12001):
      self.serverConnection = Connection()
      self.serverConnection.open(portOfServer)
    
    def listen(self):
      while(1):
        serialObj = self.serverConnection.receive() #stuck until receives a file read or write request
        requestObj = cPickle.loads(serialObj)
        if (requestObj[0] == "FFFFFFFF"): #client wants file
          self.replyF(requestObj[1])
        else: #client is posting file as ['filename', content]
          f.open(requestObj[0],'w')
          f.write(requestObj[1])
          fileConfirmation = [requestObj[0], 'confirmed']
          self.serverConnection.send(cPickle.dumps(fileConfirmation))
      
    def replyF(self, fileName):
      #Command:     post F (only for projects that support bi-directional transfers)
      #The FTA-client uploads file F to the server (if F exists in the same directory as the fta-client executable).
      f = open(fileName, 'r')
      obj = [fileName, f.read()]
      self.serverConnection.send(cPickle.dumps(obj))
    
    def terminate(self):
      #Shuts down FTA-Server gracefully
      pass 
        
if __name__ == "__main__":
  serverApp = ServerApplication()
  serverApp.openServer()
  serverApp.listen()
      