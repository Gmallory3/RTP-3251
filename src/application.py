'''
Created on Nov 17, 2014

@author: Garrett
'''

class application(object):
    '''  
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
"""   
      FTA SERVER
Command-line:   fta-server X A P
The command-line arguments are:
X: the port number at which the fta-server’s UDP socket should bind to (odd number)
A: the IP address of NetEmu
P: the UDP port number of NetEmu
Command:     window W (only for projects that support pipelined and bi-directional transfers)
W: the maximum receiver’s window-size at the FTA-Server (in segments).
Command:     terminate
Shut-down FTA-Server gracefully.

FTA CLIENT
Command-line:   fta-client X A P
The command-line arguments are:
X: the port number at which the fta-client’s UDP socket should bind to (even number). Please remember that this port number should be equal to the server’s port number minus 1.
A: the IP address of NetEmu
P: the UDP port number of NetEmu
Command:     connect-get F  (only for projects that do NOT support bi-directional transfers)
This command does two things. First, the FTA-client connects to the FTA-server and, if the connection is successfully completed, the client downloads file F from the server (if F exists in the same directory that the fta-server executable is stored at). 
If you only support uni-directional transfers (from the server to the client), the client should disconnect from the server at the end of the transfer.   
Command:     connect (only for projects that support bi-directional transfers)
The FTA-client connects to the FTA-server (running at the same IP host). 
Command:     get F (only for projects that support bi-directional transfers)
The FTA-client downloads file F from the server (if F exists in the same directory as the fta-server executable).
Command:     post F (only for projects that support bi-directional transfers)
The FTA-client uploads file F to the server (if F exists in the same directory as the fta-client executable).
Command:     window W (only for projects that support pipelined transfers)
W: the maximum receiver’s window-size at the FTA-Client (in segments).
Command:     disconnect (only for projects that support bi-directional transfers)
The FTA-client terminates gracefully from the FTA-server. 

"""
        