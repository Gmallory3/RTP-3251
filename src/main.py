# Test class
# @author aashish9patel
# @version 0.1

from connection import Connection

def client():
    clientConn = Connection('127.0.0.1')
    while 1:
        clientConn.send(raw_input('>>'));

def server():
    serverConn = Connection('127.0.0.1')
    serverConn.receive()


if __name__ == '__main__':
    print ("main")
    inp = int(raw_input('0:Client or 1:server - '))
    if(inp == 0):
        client()
    else:
        server()
