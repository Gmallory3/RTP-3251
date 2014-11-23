'''
Created on Nov 17, 2014

@author: Garrett
'''

import connection

class ClientApplication(object):
    '''  
    Used for testing the methods that will be available via the RTP-3251 API
    '''

    def __init__(self):
      f = open("file1", "r")
      print (f.read())
      
    #Client commands
    def connect(self, portOfClient=12000, destIp="143.215.129.100", destPort=7000):
      #Command:     connect (only for projects that support bi-directional transfers)
      #The FTA-client connects to the FTA-server (running at the same IP host). 
      pass
    
    def getF(self):
      #Command:     get F (only for projects that support bi-directional transfers)
      #The FTA-client downloads file F from the server (if F exists in the same directory as the fta-server executable).
      str = connectionGetFileCommand()
      f = open("file1Result", "w")
      f.write(str)
      
    def postF(self):
      #Command:     post F (only for projects that support bi-directional transfers)
      #The FTA-client uploads file F to the server (if F exists in the same directory as the fta-client executable).
      pass
    def disconnect(self):
      #Command:     disconnect (only for projects that support bi-directional transfers)
      #The FTA-client terminates gracefully from the FTA-server. 
      pass
      
      
      
if __name__ == "__main__":
  cApp = ClientApplication()
      
      
        