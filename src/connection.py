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

		#server vars


	def open(self, port, addr=('',12000), timeout=1000):
  		self.srcaddr = (addr[0], port)
		self.timeout = timeout
		pktman = PacketManager(port, )
		# server
		if(addr == ('',12000)):
			ServerManager()

			
			return self
		# client
		else:
			self.destaddr = addr
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.bind(self.srcaddr)
			tcount = 0
			while (pkt.crtlBits != 0xC):
				pkt = Packet(self.srcaddr[1], self.destaddr[1], crtlBits=0x4)
				self.send(pkt)
				t = time.clock()
				tcount = tcount + 1
				while(time.clock() - t < timeout):
					data, addr = sock.recvfrom(160)
					if(data != None):
						pkt = Packet(data)
						break
				if(tcount > 5):
					if (self._debug): print 'tcount exceeded 5'
					print 'Handshake failure! Terminating connection'
					return None
			pkt = Packet(self.srcaddr[1], self.destport,crtlBits=0x8)
			self.send(pkt)
			# return but keep a thread alive listening for 0xC because this indicates need to resend 0x8
			# only kill when data start getting ack'd
			return self

	def open_client(self, port, addr=('',12000), timeout=1000):
		pass

	def open_server(self, port, proc_addr, serverman):
		self.srcaddr = (self.srcaddr[0], port)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(self.srcaddr)
		# listen 
		while 1:
			data, addr = sock.recvfrom(160)
			if((Packet(data).crtlBits == 0x4) and (addr not in proc_addr)):
				break
		proc_addr.append(addr)
		self.destaddr = addr;
		serverman.spawn()

		pkt = Packet(data)
		tcount = 0
		while(addr == self.destaddr and pkt.crtlBits != 0x8):
			pkt = PacketManager(self.srcaddr[1], self.destaddr[1], crtlBits=0xC)
			self.send(pkt)
			t = time.clock()
			tcount = tcount + 1
			while (time.clock() - t < timeout):
				data, addr = sock.recvfrom(160)
				if(addr == self.destaddr and data != None):
					pkt = Packet(data)
					break
			if(tcount > 5):
				if (self._debug): 
					print 'tcount exceeded 5'
					print 'Handshake failure! Terminating connection'
				return
		


class ServerManager():
	def __init__(self, port):
		self.port = port
		self.shared = Manager()
		self.addrlist = shared.list([])
		self.plist = []

	#create new listening connection
	def spawn():
		self.plist.append(Process(target=aConn, args=(port)))
		self.plist[-1].start()

	#multithreaded generator method
	def aConn(port):
		c = Connection()
		c.open_server(port, self.addrlist, self)

	def kill(idx):
		self.addrlist.remove(idx)
		self.plist[idx].terminate()


	# def send(self, PKT):
	# 	if(self._debug): print "DATA:", PKT.data
	# 	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# 	sock.sendto(PKT, (self.destipaddr, self.port))

	# def receive(self, BUFFER_SIZE=1024):
	# 	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# 	sock.bind((self.srcaddr, self.srcport)) # '' indicates all available interfaces
	# 	while 1:
	# 		data, addr = sock.recvfrom(BUFFER_SIZE)
	# 		if(self._debug): print "message in:", data
	# 