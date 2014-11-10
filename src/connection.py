# Manage connection
# @author aashish9patel
# @version 0.1

import socket

class Connection():
	def __init__(self, ipaddr, port=5000, timeout=1000):
		self.ipaddr = ipaddr
		self.port = port
		self.timeout = timeout


	def send(self, MSG):
		print "message out:", MSG
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(MSG, (self.ipaddr, self.port))

	def receive(self, BUFFER_SIZE=1024):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self.ipaddr, self.port))
		while 1:
			data, addr = sock.recvfrom(BUFFER_SIZE)
			print "message in:", data