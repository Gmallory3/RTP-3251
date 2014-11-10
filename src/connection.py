# Manage connection
# @author aashish9patel
# @version 0.10a

import socket
from packet import Packet

class Connection():

	def __init__(self, _debug=True):
		self._debug = _debug
		self.destipaddr = '0.0.0.0'
		self.destport = -1
		self.srcaddr = ''
		self.srcport = -1
		self.timeout = 1000

	def open(self, port, ipaddr='0.0.0.0', timeout=1000):
		self.port = port
		self.timeout = timeout
		# server
		if(ipaddr != '0.0.0.0'):
			self.destipaddr = ipaddr
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.bind((self.srcport, self.port))
			# listen
			while 1:
				data, addr = sock.recvfrom(160)
				if(Packet(data).crtlBits == 0x4): break
			pkt = Packet(srcport, destport, crtlBits=0xC)
			send(pkt)
			# return but keep a thread alive listening for 0x4 because this indicates need to resend 0xC
			# only kill when data start getting recv'd
			self.destipaddr = addr
			self.destport = ??????
			return self
		# client
		else:
			pkt = Packet(srcport, destport,crtlBits=0x4)
			send(pkt)
			#start listener
			#start timer
			#if no response or response!=0xc resend; reset timer
			#repeat x3
			#if fail, indicate handshake fail
			#else
			pkt = Packet(srcport, destport,crtlBits=0x8)
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