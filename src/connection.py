# Manage connection
# @author aashish9patel
# @version 0.20

import socket, time
from packet import Packet, PacketManager
from multiprocessing import Process, Manager

class Connection():

	def __init__(self, _debug=True):
		self._debug = _debug
		self.destaddr = ('', -1)
		self.srcaddr = ('', -1)
		self.timeout = 1000

		#server vars
		self.servermanager = None

	# Generic open connection
	def open(self, port, addr=('',12000), timeout=1000):
		self.timeout = timeout
		# server
		if(addr == ('',12000)):
			self.servermanager = ServerManager(port)
			return
		# client
		else:
			Process(target=open_client, args=(port, addr, timeout))
			return

	# Start the client connection
	def open_client(self, port, addr):
		self.srcaddr = (srcaddr[0], port)
		self.destaddr = addr
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(self.srcaddr)
		pacman = PacketManager(self.srcaddr[1], self.destaddr[1])
		while(1):
			pacman.addOutgoing(crtlBits=0x4)
			self.send(pacman.outgoingBFR[0])
			pacman.outgoingBFR[0] = (pacman.outgoingBFR[0][0], time.clock(), pacman.outgoingBFR[0][2]+1)
			if(pacman.outgoingBFR[0][2] > 5):
				if (self._debug):
					print ('send count exceeded 5')
					print ('Handshake failure! Terminating connection')
				return

			while(time.clock() - pacman.outgoingBFR[0][1] < self.timeout):
				data, addr = sock.recvfrom(160)
				if(addr == self.destaddr and data != None):
					if(PacketManager.stringToPacket(data).crtlBits == 0xC):
						pacman.outgoingBFR[0] = (pacman.outgoingBFR[0][0], time.clock(), 0)
						break
		pacman.addOutgoing(crtlBits=0x8)
		self.KeepAlive(sock, pacman)
		

	def open_server(self, port, proc_addr):
		self.srcaddr = (self.srcaddr[0], port)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(self.srcaddr)
		# listen 
		while 1:
			data, addr = sock.recvfrom(160)
			pkt = PacketManager.stringToPacket(data)
			if((pkt.crtlBits == 0x4) and (addr not in proc_addr)):
				break
		proc_addr.append(addr)
		self.destaddr = addr;
		self.servermanager.spawn()
		
		pacman = PacketManager(self.srcaddr[1], self.destaddr[1])
		while(addr == self.destaddr and pkt.crtlBits != 0x8):
			pkt = pacman.addOutgoing(crtlBits=0xC)
			self.send(pacman.outgoingBFR[0])
			pacman.outgoingBFR[0] = (pacman.outgoingBFR[0][0], time.clock(), pacman.outgoingBFR[0][2]+1)
			if(pacman.outgoingBFR[0][2] > 5):
				if (self._debug):
					print ('send count exceeded 5')
					print ('Handshake failure! Terminating connection')
				return
			while (time.clock() - pacman.outgoingBFR[0][1] < self.timeout):
				data, addr = sock.recvfrom(160)
				if(addr == self.destaddr and data != None):
					pkt = pacman.addIncoming(data)
					break
		pacman.outgoingBFR.remove(0)
		self.KeepAlive(sock, pacman)

	# KEEPALIVE
	def KeepAlive(self, sock, pacman):
		while(1):
			# INCOMING
			data, addr = sock.recvfrom(BUFFER_SIZE)
			if(addr == self.destaddr):
				# client: server didnt get 0x8
				if((PacketManager.stringToPacket(data).crtlBits == 0xC) and (PacketManager.stringToPacket(pacman.outgoingBFR[0][0]).crtlBits == 0x8)):
					self.send(pacman.outgoingBFR[0])
					pacman.outgoingBFR[0] = (pacman.outgoingBFR[0][0], time.clock(), pacman.outgoingBFR[0][2]+1)
					# reset counts to 0
					if(len(pacman.outgoingBFR) > 1):
						for i in range(1, len(pacman.outgoingBFR)+1):
							pacman.outgoingBFR[i] = (pacman.outgoingBFR[i][0], time.clock(), 0)
					if(pacman.outgoingBFR[0][2] > 5):
						if (self._debug):
							print ('Handshake failure! Terminating connection')
						return
					continue
				#server: client ack'd handshake, so remove 0xC
				elif(PacketManager.stringToPacket(data).crtlBits == 0x8):
					pacman.outgoingBFR.remove(0)
				else:
					pacman.addIncoming(data)
			#OUTGOING
			pop = False
			if(len(pacman.outgoingBFR) > 0):
				for i in range(0, len(pacman.outgoingBFR)+1):
					if((pacman.outgoingBFR[i][1] == -1) or (time.clock - pacman.outgoingBFR[i][1] > self.timeout)):
						#Client ACK still in outgoing buffer
						if(PacketManager.stringToPacket(pacman.outgoingBFR[i][0]).crtlBits == 0x8):
							pacman.outgoingBFR[i] = (pacman.outgoingBFR[i][0], time.clock(), pacman.outgoingBFR[i][2]+1)
							if(pacman.outgoingBFR[i][2] > 5):
								pop = True
							continue
						self.send(pacman.outgoingBFR[i])
						pacman.outgoingBFR[i] = (pacman.outgoingBFR[i][0], time.clock(), pacman.outgoingBFR[i][2]+1)
				if(pop):
					pacman.outgoingBFR.remove(0)

	#send over UDP
	def send(self, PKT):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self.srcaddr[0], port))
		if(self._debug): print ('DATA: ', PKT.data)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(PKT,  PKT)

	def receive(self, BUFFER_SIZE=1024):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self.srcaddr, self.srcport)) # '' indicates all available interfaces
		while 1:
			data, addr = sock.recvfrom(BUFFER_SIZE)
			if(self._debug): print ('message in:', data)


class ServerManager():
	def __init__(self, port):
		self.port = port
		self.shared = Manager()
		self.addrlist = self.shared.list([])
		self.plist = []
		self.spawn()

	#create new listening connection
	def spawn(self):
		self.plist.append(Process(target=self.aConn, args=(self.port, )))
		self.plist[-1].start()

	#multithreaded generator method
	def aConn(port):
		c = Connection()
		c.open_server(port, self.addrlist)

	#kill process
	def kill(idx):
		self.addrlist.remove(idx)
		self.plist[idx].terminate()
