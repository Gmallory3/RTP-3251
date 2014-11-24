# Manage connection
# @author aashish9patel
# @version 0.20

import socket, time
from packet import Packet
from packet import PacketManager
from multiprocessing import Process
#, Manager

class Connection():

	def __init__(self, _debug=True):
		self._debug = _debug
		self.destaddr = ('', -1)
		self.srcaddr = ('', -1)
		self.sockettimeout = 1  #in FREAKING SECONDS!!
		self.timeout = 1 # IN SECONDS AS WELL
		self.pacman = None

	# Generic open connection
	def open(self, port, addr=('',12000), timeout=1000):
		if(port > 65535 and addr[1] > 65535):
			print ('PORT OUT OF RANGE')
			return
		if(len(addr) != 2):
			print ('ADDR INCORRECTLY FORMATTED')
			return
		self.timeout = timeout
		# server
		if(addr == ('',12000)):
			Process(target=self.open_server, args=(port, )).start()
			return
		# client
		else:
			Process(target=self.open_client, args=(port, addr)).start()
			return

	# Send stuff
	def send(self, obj):
		self.pacman.addOutgoingFile(data=obj)

	# Receive stuff
	def receive(self):
		while(len(pacman.applicationBFR) == 0): pass
		retVal = pacman.applicationBFR[0]
		pacman.applicationBFR.pop(0)
		return retVal


	# End connection
	def terminate(self):
		pass

	# Start the client connection
	def open_client(self, port, addr):
		self.srcaddr = (self.srcaddr[0], port)
		self.destaddr = addr
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.settimeout(self.sockettimeout)
		sock.bind(self.srcaddr)
		self.pacman = PacketManager(self.srcaddr[1], self.destaddr[1])
		self.pacman.addOutgoing(ctrlBits=0x4)
		while(len(self.pacman.outgoingBFR) > 0):
			sock.sendto(self.pacman.outgoingBFR[0][0], self.destaddr)
			if(self._debug): print ('OUTGOING', self.pacman.stringToPacket(self.pacman.outgoingBFR[0][0]).ctrlBits)
			self.pacman.outgoingBFR[0] = (self.pacman.outgoingBFR[0][0], time.clock(), self.pacman.outgoingBFR[0][2]+1)
			if(self.pacman.outgoingBFR[0][2] > 5):
				if (self._debug):
					print ('send count exceeded 5')
					print ('Handshake failure! Terminating connection')
				return
			exitwhile = False
			while(time.clock() - self.pacman.outgoingBFR[0][1] < self.timeout):
				try:
					data, addr = sock.recvfrom(160)
					if(addr == self.destaddr and data != None):
						if(self._debug): print ('INCOMING', self.pacman.stringToPacket(data).ctrlBits)
						if(self.pacman.stringToPacket(data).ctrlBits == 0xC):
							self.pacman.outgoingBFR.pop(0)
							exitwhile = True
							break
				except socket.timeout:
					pass
				if(exitwhile): break

		self.pacman.addOutgoing(ctrlBits=0x8)
		sock.sendto(self.pacman.outgoingBFR[0][0], self.destaddr)
		if(self._debug): print ('OUTGOING', self.pacman.stringToPacket(self.pacman.outgoingBFR[0][0]).ctrlBits)
		self.pacman.outgoingBFR[0] = (self.pacman.outgoingBFR[0][0], time.clock(), self.pacman.outgoingBFR[0][2]+1)
		self.KeepAlive(sock)
		

	def open_server(self, port):
		self.srcaddr = (self.srcaddr[0], port)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.settimeout(self.sockettimeout)
		sock.bind(self.srcaddr)
		self.pacman = PacketManager(-1, -1)
		# listen 
		exitwhile = False
		while 1:
			try:
				data, addr = sock.recvfrom(160)
				pkt = self.pacman.stringToPacket(data)
				if((pkt.ctrlBits == 0x4)):
					if(self._debug): print ('INCOMING', pkt.ctrlBits)
					exitwhile = True
					break
			except socket.timeout:
				pass
			if(exitwhile): break

		self.destaddr = addr

		self.pacman.sourcePort = self.srcaddr[1]
		self.pacman.destinationPort = self.destaddr[1]

		while(pkt.ctrlBits != 0x8):
			self.pacman.addOutgoing(ctrlBits=0xC)
			sock.sendto(self.pacman.outgoingBFR[0][0], self.destaddr)
			if(self._debug): print ('OUTGOING', self.pacman.stringToPacket(self.pacman.outgoingBFR[0][0]).ctrlBits)
			self.pacman.outgoingBFR[0] = (self.pacman.outgoingBFR[0][0], time.clock(), self.pacman.outgoingBFR[0][2]+1)
			if(self.pacman.outgoingBFR[0][2] > 5):
				if (self._debug):
					print ('send count exceeded 5')
					print ('Handshake failure! Terminating connection')
				return
			exitwhile = False
			while (time.clock() - self.pacman.outgoingBFR[0][1] < self.timeout):
				try:
					data, addr = sock.recvfrom(160)
					if(addr == self.destaddr):
						pkt = self.pacman.stringToPacket(data)
						if(self._debug): print ('INCOMING', pkt.ctrlBits)
						exitwhile = True
						break
				except socket.timeout:
					pass
				if(exitwhile): break
		self.pacman.outgoingBFR.pop(0)
		if(self._debug): print ('EST')
		self.KeepAlive(sock)

	# SERVER & CLIENT KEEPALIVE
	def KeepAlive(self, sock):
		while(1):
			try:
				data, addr = sock.recvfrom(self.pacman.BUFFER_SIZE)
				#INCOMING
				if(addr == self.destaddr):
					# client: server didnt get 0x8
					if((self.pacman.stringToPacket(data).ctrlBits == 0xC) and (self.pacman.stringToPacket(self.pacman.outgoingBFR[0][0]).ctrlBits == 0x8)):
						if(self._debug): print ('INCOMING', self.pacman.stringToPacket(data).ctrlBits)
						sock.sendto(self.pacman.outgoingBFR[0][0], self.destaddr)
						if(self._debug): print ('OUTGOING', self.pacman.stringToPacket(self.pacman.outgoingBFR[0][0]).ctrlBits)
						self.pacman.outgoingBFR[0] = (self.pacman.outgoingBFR[0][0], time.clock(), self.pacman.outgoingBFR[0][2]+1)
						# reset counts to 0
						if(len(self.pacman.outgoingBFR) > 1):
							for i in range(1, len(self.pacman.outgoingBFR)+1):
								self.pacman.outgoingBFR[i] = (self.pacman.outgoingBFR[i][0], time.clock(), 0)
						if(self.pacman.outgoingBFR[0][2] > 5):
							if (self._debug):
								print ('Handshake failure! Terminating connection')
							return
						continue
					#server: client ack'd handshake, so pop 0xC
					elif(self.pacman.stringToPacket(data).ctrlBits == 0x8):
						if(self._debug): print ('INCOMING', self.pacman.stringToPacket(data).ctrlBits)
						self.pacman.outgoingBFR.pop(0)
					else:
						if(self._debug): print ('INCOMING data')
						self.pacman.addIncoming(data)
			except socket.timeout:
				#OUTGOING
				pop = False
				if(len(self.pacman.outgoingBFR) > 0):
					for i in range(0, len(self.pacman.outgoingBFR)):
						if((self.pacman.outgoingBFR[i][1] == -1) or (time.clock() - self.pacman.outgoingBFR[i][1] > self.timeout)):
							#Client ACK still in outgoing buffer
							if(self.pacman.stringToPacket(self.pacman.outgoingBFR[i][0]).ctrlBits == 0x8):
								self.pacman.outgoingBFR[i] = (self.pacman.outgoingBFR[i][0], time.clock(), self.pacman.outgoingBFR[i][2]+1)
								if(self.pacman.outgoingBFR[i][2] > 5):
									pop = True
								continue
							sock.sendto(self.pacman.outgoingBFR[i][0], self.destaddr)
							if(self._debug): print ('OUTGOING')
							self.pacman.outgoingBFR[i] = (self.pacman.outgoingBFR[i][0], time.clock(), self.pacman.outgoingBFR[i][2]+1)
					if(pop):
						self.pacman.outgoingBFR.pop(0)
