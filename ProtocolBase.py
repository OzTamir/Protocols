import socket
import ssl
import getpass

class ProtocolBase(object):
	def __init__(self, server, port, debug=False):
		''' Open socket and login to the server '''
		self.server = server
		self.port = int(port)
		self.username = ''
		self.password = ''
		self.debug = debug

	def get_socket(self, SSL_required=True):
		''' Create a socket (SSL enabled by default) '''
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.server, self.port))
		if SSL_required:
			ssl_socket = ssl.wrap_socket(sock)
			return ssl_socket
		return sock

	def read(self, debug=None):
		''' Read data from the server '''
		if debug is None:
			debug = self.debug
		data = ''
		while True:
			next = self.sock.recv(1)
			# Read data until a newline is reached
			if next == '\n' or data[-2::] == '\r\n':
				break
			data += next
		if self.debug and debug:
			print data
		return data

	def send(self, cmd, data='', read_at_end=False):
		''' Send a command to the email server '''
		# Compile the message that will be sent to the server
		if data == '':
			packet = '%(CMD)s\r\n' % {'CMD' : cmd.upper()}
		else:
			packet = '%(CMD)s %(DATA)s\r\n'	% {'CMD' : cmd.upper(), 'DATA' : str(data)}
		self.sock.send(packet)
		# We want this to happen to avoid messages getting 'stuck in the pipe'
		if read_at_end:
			self.read()