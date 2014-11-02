'''
Created on Nov 2, 2014

@author: Garrett
'''

class Packet():
    
    def __init__(self, sourcePort=12000, destinationPort=12000, sequenceNumber=0, acknowledgmentNumber=0, 
                 window=10, checksum=None, crtlBits=0x000, offset=None, options=None, padding=None, data=None):
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.sequenceNumber = sequenceNumber
        self.acknowlgmentNumber = acknowledgmentNumber
        self.window = window
        self.checksum = checksum
        self.crtlBits = crtlBits
        self.offset = offset
        self.options = options
        self.padding = padding
        self.data = data
        
        #Note, only crtlBits are stored as bits on Nov 2. This will likely change.


if __name__ == '__main__':
    print ("Testing main")