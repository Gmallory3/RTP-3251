# Manage connection
# @author aashish9patel
# @version 0.10a

import socket, time
from packet import Packet

class Connection():

	def __init__(self, _debug=True):
		self._debug = _debug
		self.destaddr = ('', -1)
		self.srcaddr = ('', -1)
		self.timeout = 1000
		self.processes = [(None, None), ]

	def open(self, port, addr=('',12000), timeout=1000):
		self.srcaddr = (addr[0], port)
		self.timeout = timeout
		pkt = Packet()
		# server (should be listening, spawn processes based on connection requests)
		if(addr == ('',12000)):
			self.destaddr = ('', -1)
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.bind(self.srcaddr)
			# listen 
			#todo move this to a thread
			while 1:
				data, addr = sock.recvfrom(160)
				if(Packet(data).crtlBits == 0x4): break
			tcount = 0
			while (pkt.crtlBits != 0x8):
				pkt = Packet(self.srcaddr[1], self.destaddr[1], crtlBits=0xC)
				send(pkt)
				t = time.clock()
				tcount++
				while (time.clock() - t < timeout):
					data, addr = sock.recvfrom(160)
					if(data != None && Packet(data).crtlBits == 0x8):
						pkt = Packet(data)
						break
				if(tcount > 5):
					if (self._debug): print 'tcount exceeded 5'
					print 'Handshake failure! Terminating connection'
					return None
			self.destaddr = addr
			return self
		# client
		else:
			self.destaddr = addr
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.bind(self.srcaddr)
			tcount = 0
			while (pkt.crtlBits != 0xC):
				pkt = Packet(self.srcaddr[1], self.destaddr[1], crtlBits=0x4)
				send(pkt)
				t = time.clock()
				tcount++
				while(time.clock() - t < timeout):
					data, addr = sock.recvfrom(160)
					if(data != None):
						pkt = Packet(data)
						break
				if(tcount > 5):
					if (self._debug): print 'tcount exceeded 5'
					print 'Handshake failure! Terminating connection'
					return None
			pkt = Packet(self.srcaddr[1], destport,crtlBits=0x8)
			send(pkt)
			# return but keep a thread alive listening for 0xC because this indicates need to resend 0x8
			# only kill when data start getting ack'd

			return self



	def send(self, PKT):
		if(self._debug): print "DATA:", PKT.data
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(PKT, (self.destipaddr, self.port))

	def receive(self, BUFFER_SIZE=1024):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self.srcaddr, self.srcport)) # '' indicates all available interfaces
		while 1:
			data, addr = sock.recvfrom(BUFFER_SIZE)
			if(self._debug): print "message in:", data