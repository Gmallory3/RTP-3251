# Manage connection
# @author aashish9patel, gmallory
# @version 0.51

import socket, time, sys
from packet import Packet
from packet import PacketManager
from multiprocessing import Process, Queue
#, Manager

class Connection():
	def __init__(self, _debug=True):
		self._debug = _debug
		self.destaddr = ('', -1)
		self.srcaddr = ('', -1)
		self.sockettimeout = 1  #in FREAKING SECONDS!!
		self.timeout = 1 # IN SECONDS AS WELL
		self.pacman = PacketManager(-1,-1)
		self.connType = None # 0 client 1 server
		self.queue = (Queue(), Queue()) # (in2KA, out2KA)
		self.connEst = False

	# Generic open connection
	def open(self, port, addr=('',12000), timeout=1):
		if(port > 65535 and addr[1] > 65535):
			print ('PORT OUT OF RANGE')
			return
		if(len(addr) != 2):
			print ('ADDR INCORRECTLY FORMATTED')
			return
		self.timeout = timeout
		# server
		if(addr == ('',12000)):
			self.connType = 1
			Process(target=self.open_server, args=(port, self.queue)).start()
			return
		# client
		else:
			self.connType = 0
			Process(target=self.open_client, args=(port, addr, self.queue)).start()
			return

	# Send stuff
	def send(self, obj, timeout=10):
		t = time.clock()
		while(not self.connEst and time.clock()-t < timeout):
			if(not self.queue[1].empty()):
				q = self.queue[1].get()
				if(q == (1, )): self.connEst = 1
				else: self.queue[1].put(q)
		if(not self.connEst):
			return
		self.queue[0].put((2, obj))

	# Receive stuff
	def receive(self, timeout = 10):
		t = time.clock()
		while(time.clock() - t < timeout): 
			if(not self.queue[1].empty()):
				q = self.queue[1].get()
				if(q == (1, )):
					self.connEst = 1
					continue
				return q


	# End connection
	def terminate(self):
		self.queue[0].put((1, ))

	# Start the client connection
	def open_client(self, port, addr, queue):
		self.srcaddr = (self.srcaddr[0], port)
		self.destaddr = addr
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.settimeout(self.sockettimeout)
		sock.bind(self.srcaddr)
		self.pacman.sourcePort = self.srcaddr[1]
		self.pacman.destinationPort = self.destaddr[1]
		self.pacman.addOutgoing(ctrlBits=0x4)
		while(len(self.pacman.outgoingBFR) > 0):
			sock.sendto(self.pacman.outgoingBFR[0][0], self.destaddr)
			if(self._debug): print ('83 OUTGOING', self.pacman.stringToPacket(self.pacman.outgoingBFR[0][0]).ctrlBits)
			self.pacman.outgoingBFR[0] = (self.pacman.outgoingBFR[0][0], time.clock(), self.pacman.outgoingBFR[0][2]+1)
			if(self.pacman.outgoingBFR[0][2] > 5):
				self.timeout+=0.5
				self.sockettimeout+=0.5
				sock.settimeout(self.sockettimeout)
				if(self.pacman.outgoingBFR[0][2] > 10):
					if (self._debug):
						print ('send count exceeded 10')
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
		if(self._debug): print ('106 OUTGOING', self.pacman.stringToPacket(self.pacman.outgoingBFR[0][0]).ctrlBits)
		self.pacman.outgoingBFR[0] = (self.pacman.outgoingBFR[0][0], time.clock(), self.pacman.outgoingBFR[0][2]+1)
		self.KeepAlive(sock, queue)
		return
		

	def open_server(self, port, queue):
		self.srcaddr = (self.srcaddr[0], port)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.settimeout(self.sockettimeout)
		sock.bind(self.srcaddr)
		self.pacman = PacketManager(-1, -1)
		# listen 
		exitwhile = False
		if(self._debug): print ('Listening...')
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
			if(self._debug): print ('141 OUTGOING', self.pacman.stringToPacket(self.pacman.outgoingBFR[0][0]).ctrlBits)
			self.pacman.outgoingBFR[0] = (self.pacman.outgoingBFR[0][0], time.clock(), self.pacman.outgoingBFR[0][2]+1)
			if(self.pacman.outgoingBFR[0][2] > 5):
				self.timeout+= 0.5
				self.sockettimeout+=0.5
				sock.settimeout(self.sockettimeout)
				if(self.pacman.outgoingBFR[0][2] > 10):
					if (self._debug):
						print ('send count exceeded 10')
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
		remove = []
		for n,i in enumerate(self.pacman.outgoingBFR):
			if(self.pacman.stringToPacket(i[0]).ctrlBits == 0xc):
				remove.append(n)
		remove.reverse()
		for i in remove:
			self.pacman.outgoingBFR.pop(i)
		del remove[:]
		if(self._debug): print ('EST')
		self.KeepAlive(sock, queue)
		return

	# SERVER & CLIENT KEEPALIVE
	def KeepAlive(self, sock, queue):
		q = None
		queue[1].put((1, ))
		while(1):
			#print len(self.pacman.outgoingBFR), len(self.pacman.tmpIncomingBFR), len(self.pacman.applicationBFR), [self.pacman.stringToPacket(i[0]).ctrlBits for i in self.pacman.outgoingBFR]
			#print "\t", [self.pacman.stringToPacket(i[0]).data for i in self.pacman.outgoingBFR]
			#print "\t", [(i[0], i[2]) for i in self.pacman.tmpIncomingBFR]
			#incoming parameters
			if(not queue[0].empty()): 
				q = queue[0].get()
			else: 
				q = None
			if(q != None and type(q) == tuple):
				if(q[0] == 1):
					self.pacman.addOutgoing(ctrlBits=0x2)
					sock.sendto(self.pacman.outgoingBFR[-1][0], self.destaddr)
					if(self._debug): print ('OUTGOING FIN')
					self.pacman.outgoingBFR[-1] = (self.pacman.outgoingBFR[-1][0], time.clock(), self.pacman.outgoingBFR[-1][2]+1)
				elif(q[0] == 2):
					self.pacman.addOutgoingFile(dataIn=q[1])
			#outgoing parameters
			if(len(self.pacman.applicationBFR) > 0):
				queue[1].put(self.pacman.applicationBFR[0])
				self.pacman.applicationBFR.pop(0)
			try:
				data, addr = sock.recvfrom(self.pacman.BUFFER_SIZE)
				#INCOMING
				if(addr == self.destaddr):
					# client: server didnt get 0x8
					if((self.pacman.stringToPacket(data).ctrlBits == 0xC) and len(self.pacman.outgoingBFR) > 0 and (self.pacman.stringToPacket(self.pacman.outgoingBFR[0][0]).ctrlBits == 0x8)):
						if(self._debug): print ('INCOMING', self.pacman.stringToPacket(data).ctrlBits)
						sock.sendto(self.pacman.outgoingBFR[0][0], self.destaddr)
						if(self._debug): print ('204 OUTGOING', self.pacman.stringToPacket(self.pacman.outgoingBFR[0][0]).ctrlBits)
						self.pacman.outgoingBFR[0] = (self.pacman.outgoingBFR[0][0], time.clock(), self.pacman.outgoingBFR[0][2]+1)
						# reset counts to 0
						if(len(self.pacman.outgoingBFR) > 1):
							for i in range(1, len(self.pacman.outgoingBFR)):
								self.pacman.outgoingBFR[i] = (self.pacman.outgoingBFR[i][0], time.clock(), 0)
						if(self.pacman.outgoingBFR[0][2] > 5):
							self.timeout+= 0.5
							self.sockettimeout+=0.5
							sock.settimeout(self.sockettimeout)
							if(self.pacman.outgoingBFR[0][2] > 10):
								if (self._debug):
									print ('send count exceeded 10')
									print ('Handshake failure! Terminating connection')
								return
						#continue
					#server: client ack'd handshake, so pop 0xC
					# elif(self.pacman.stringToPacket(data).ctrlBits == 0x8):
					# 	if(self._debug): print ('INCOMING', self.pacman.stringToPacket(data).ctrlBits)
					# 	self.pacman.addIncoming(data)
					#FIN
					elif(self.pacman.stringToPacket(data).ctrlBits == 0x2):
						if(self._debug): print ('INCOMING FIN')
						del self.pacman.outgoingBFR[:]
						self.pacman.addOutgoing(ctrlBits=0xA)
						while(self.pacman.outgoingBFR[0][2] < 5):
							if((self.pacman.outgoingBFR[0][1] == -1) or (time.clock() - self.pacman.outgoingBFR[0][1] > self.timeout)):
								sock.sendto(self.pacman.outgoingBFR[0][0], self.destaddr)
								if(self._debug): print ('227 OUTGOING FIN ACK')
								self.pacman.outgoingBFR[0] = (self.pacman.outgoingBFR[0][0], time.clock(), self.pacman.outgoingBFR[0][2]+1)
						return
					elif(self.pacman.stringToPacket(data).ctrlBits == 0xA):
						if(self._debug): print ('INCOMING FIN ACK')
						return
					#data
					else:
						if(self._debug): print ('INCOMING data')
						self.pacman.addIncoming(data)
			except socket.timeout:
				pass
			finally:
				#OUTGOING
				remove = []
				if(len(self.pacman.outgoingBFR) > 0):
					win = min(len(self.pacman.outgoingBFR), self.pacman.window)
					for i in range(0, len(self.pacman.outgoingBFR)):
						if((self.pacman.outgoingBFR[i][1] == -1) or (time.clock() - self.pacman.outgoingBFR[i][1] > self.timeout)):
							sock.sendto(self.pacman.outgoingBFR[i][0], self.destaddr)
# 							print("print at 246",self.pacman.stringToPacket(self.pacman.outgoingBFR[i][0]).ctrlBits)
# 							print("print at 246",self.pacman.stringToPacket(self.pacman.outgoingBFR[i][0]).acknowledgmentNumber)

							#Client ACK still in outgoing buffer
							if (self.pacman.stringToPacket(self.pacman.outgoingBFR[i][0]).ctrlBits == 0x8 and self.pacman.stringToPacket(self.pacman.outgoingBFR[i][0]).acknowledgmentNumber == 0):
									self.pacman.outgoingBFR[i] = (self.pacman.outgoingBFR[i][0], time.clock(), self.pacman.outgoingBFR[i][2]+1)
									if (self.pacman.outgoingBFR[i][2] > 5):
										remove.append(i)
							elif(self.pacman.stringToPacket(self.pacman.outgoingBFR[i][0]).ctrlBits == 0x8):
								remove.append(i)
# 							if(self._debug): print ('253 OUTGOING')
							self.pacman.outgoingBFR[i] = (self.pacman.outgoingBFR[i][0], time.clock(), self.pacman.outgoingBFR[i][2]+1)
					if(len(remove) > 0):
						remove.reverse()
						for i in remove:
							self.pacman.outgoingBFR.pop(i)
						del remove[:]