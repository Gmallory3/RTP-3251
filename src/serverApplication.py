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
      
    def connect(self, portOfServer=12001, destIp="143.215.129.100", destPort=7000):
      self.serverConnection = Connection()
      self.serverConnection.open(portOfServer)
    
    def listen(self):
      requestStr = self.serverConnection.receive() #stuck until receives a file read or write request
      
    def getF(self, fileName):
      #Command:     get F (only for projects that support bi-directional transfers)
      #The FTA-client downloads file F from the server (if F exists in the same directory as the fta-server executable).
      fileRequestStr = str(0xFFFFFFFF)+ fileName
      print(fileRequestStr)
      self.clientConnection.send(fileRequestStr)
      
      serialObj = self.clientConnection.receive()
      f = open("fileResult", "w")
      f.write(cPickle.loads(serialObj)[0]) 
      
    def postF(self, fileName):
      #Command:     post F (only for projects that support bi-directional transfers)
      #The FTA-client uploads file F to the server (if F exists in the same directory as the fta-client executable).
      f = open(fileName, 'r')
      obj = [f.read()]
      serialObj = cPickle.dumps(obj)
      self.clientConnection.send(serialObj)
    
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
      
        
if __name__ == "__main__":
  serverApp = ServerApplication()
  serverApp.connect()
  fileRequestStr = str(0xFFFFFFFF) + 'file1'
  print(fileRequestStr)
      