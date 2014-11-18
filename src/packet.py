'''
Created on Nov 2, 2014

@author: Garrett
'''

class Packet():
    
    def __init__(self, sourcePort=12000, destinationPort=12000, sequenceNumber=0, acknowledgmentNumber=0, 
                 window=10, ctrlBits=0x0, options=None, data=None):
        self.sourcePort = sourcePort
        self.destinationPort = destinationPort
        self.window = window
        self.ctrlBits = ctrlBits
        self.options = options
        self.data = data
        # todo these needs to happen automatically based on data
        self.sequenceNumber = sequenceNumber #this should be either automatic (smarter than default 0) or set by param
        self.acknowlgmentNumber = acknowledgmentNumber #this should be either automatic (smarter than default 0) or set by param
        self.checksum = checksum
        self.offset = offset
        self.padding = padding 
