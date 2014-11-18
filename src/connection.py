# Manage connection
# @author aashish9patel
# @version 0.10a

import socket, time
from packet import Packet
from test.test_finalization import SelfCycleBase
import random
import math
from asyncio.tasks import _DEBUG


class Connection():

	def __init__(self, _debug=True):
		self._debug = _debug
		self.destaddr = ('', -1)
		self.srcaddr = ('', -1)
		self.timeout = 1000

	def open(self, port, addr=('',12000), timeout=1000):
		self.srcaddr = (self.addr[0], port)
  	self.srcaddr = (addr[0], port)
		self.timeout = timeout
		pkt = Packet()
		# server
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
				self.send(pkt)
				t = time.clock()
				tcount = tcount + 1
				while (time.clock() - t < timeout):
					data, addr = sock.recvfrom(160)
					if(data != None):
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
			
	
	
	
	def encrypt(self, message):
		publicKey = self.RSA()
		return message**publicKey[1]%publicKey[0]
			
	def decrypt(self, privateKey):
		return privateKey[1]%privateKey[0]
			
	"""
	RSA algorithm used for encryption.
	https://en.wikipedia.org/wiki/RSA_(cryptosystem)
	"""
	def RSA(self):
		#allows for seeding RSA with known values for testing if values supplied.
		if (_DEBUG == True):
			p = 61
			q = 53
		else:
			# 1: Calculate 2 large, random primes
			while True:
				p = random.randrange(1000000, 999999999, 2)
				if all(p % n != 0 for n in range(3, int((math.sqrt(p) + 1), 2))):
					break
			while True:
				q = random.randrange(1000000, 999999999, 2)
				if all(q % n != 0 for n in range(3, int((math.sqrt(q) + 1), 2))):
					break
		
		# 2: Compute n = p*q
		n = p*q
		
		# 3: Compute Euler's totient function =  n -(p + q -1)
		euler = (p-1)*(q-1)
		
		# 4: Chose integer e such that 1 < e < euler & gcd (e, euler)) = 1
		while True:
			e = random.randrange(1, euler, 2)
			if all(e % n != 0 for n in range(3, int((math.sqrt(e) + 1), 2))):
				# e is prime. now if e is not divisor of 3120, we're good.
				if (euler%e == 0):
					break
		
		# 5: Determine d =- e^-1 mod(euler) (I.e. solve d * e =- 1(mod(euler))
		d = self.modinv(e, euler)
		
		publicKey = (n, e)
		privateKey = (n, d)
		if (_DEBUG == True):
			print ("n: " + n)
			print ("euler: " + euler)
			print ("e: " + e)
			print ("d: " + d)
		return publicKey
	
	#####
	"""
	NOTE: THE FOLLOWING TWO METHODS (egcd, modinv) ARE FROM https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
	AND ARE SUBJECT TO REVIEW
	"""
	####
	def egcd(self, a, b):
		if a == 0:
			return (b, 0, 1)
		else:
			g, y, x = self.egcd(b % a, a)
			return (g, x - (b // a) * y, y)

	def modinv(self, a, m):
		g, x, y = self.egcd(a, m)
		if g != 1:
			raise Exception('modular inverse does not exist')
		else:
			return x % m
		
			
		