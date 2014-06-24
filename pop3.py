import socket
import ssl



class EmailClient:
	''' A POP3-Based Email reader with SSL '''
	def __init__(self, user, pwd, debug=False):
		''' Open socket and login to the server '''
		self.server = 'pop.gmail.com'
		self.port = 995
		self.username = user
		self.password = pwd
		self.debug = debug
		self.sock = self.get_socket()
		self.login(sock, user, pwd, debug)

	def get_socket(self, SSL_required=True):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.server, self.port))
		if SSL_required:
			ssl_socket = ssl.wrap_socket(sock)
			return ssl_socket
		return sock

	def read(self):
		data = ''
		while True:
			next = self.sock.recv(1)
			if next == '\n':
				break
			data += next
		if self.debug:
			print data
		return data

	def send(self, cmd, data='', read_at_end=True):
		if data == '':
			packet = '%(CMD)s\r\n' % {'CMD' : cmd.upper}
		else:
			packet = '%(CMD)s %(DATA)s\r\n'	% {'CMD' : cmd.upper(), 'DATA' : str(data)}
		self.sock.send(packet)
		if read_at_end:
			self.read()

	def login(self):
		self.read()
		self.send('USER', self.username)
		self.send('PASS', self.password)
		return

	def quit(self):
		self.send('QUIT')

	def get_mail(self):
		sock.send('STAT')
		data = read(sock).split(' ')
		print 'There are %s mails in your inbox.' % data[1]


def main():
	pass


if __name__ == '__main__':
	main()