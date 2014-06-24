import socket
import ssl
import re
import getpass


def print_seperetor():
	print '---------------------'

class POPRReader:
	''' A POP3-Based Email reader with SSL '''
	def __init__(self, user, pwd, debug=False):
		''' Open socket and login to the server '''
		self.server = 'pop.gmail.com'
		self.port = 995
		self.username = user
		self.password = pwd
		self.debug = debug
		self.sock = self.get_socket()
		self.login()

	def get_socket(self, SSL_required=True):
		''' Create a socket (SSL enabled by default) '''
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.server, self.port))
		if SSL_required:
			ssl_socket = ssl.wrap_socket(sock)
			return ssl_socket
		return sock

	def read(self, debug=None):
		''' Read data from the email server '''
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
		''' Send a POP3 command to the email server '''
		# Compile the message that will be sent to the server
		if data == '':
			packet = '%(CMD)s\r\n' % {'CMD' : cmd.upper()}
		else:
			packet = '%(CMD)s %(DATA)s\r\n'	% {'CMD' : cmd.upper(), 'DATA' : str(data)}
		self.sock.send(packet)
		# We want this to happen to avoid messages getting 'stuck in the pipe'
		if read_at_end:
			self.read()

	def login(self):
		''' Login to the server '''
		# Read the session header (the server connection confirmation)
		self.read()
		# Send the username and password (login)
		self.send('USER', self.username, True)
		self.send('PASS', self.password, True)
		return

	def quit(self):
		''' End the session '''
		self.send('QUIT')

	def get_mail_amount(self):
		''' Fetch the available mails waiting to be read '''
		self.send('STAT')
		data = self.read().split(' ')
		print 'There are %s mails in your inbox.' % data[1]
		print_seperetor()
		return int(data[1])

	def parse_header(self):
		''' Return a dictionary with email header '''
		header = dict()
		# Flush out the +OK response
		self.read(False)
		while True:
			next = self.read(False)
			if next[0] == '.':
				break
			elif next[:2] == '--':
				continue
			else:
				next = next.split(': ')
				header[next[0]] = ''.join([char for char in next[1::]]).replace('\r', '')
		return header


	def list_mails(self):
		amount = self.get_mail_amount()
		for i in range(amount):
			self.send('TOP', str(i + 1) + ' 1')
			header = self.parse_header()
			print 'Subject: %s' % header.get('Subject', 'NULL')
			print 'Sender: %s' % header.get('From', 'NULL')
			print_seperetor()




def main():
	username = raw_input('Please Enter Your Username: ')
	pwd = getpass.getpass('Please Enter Password: ')
	mail = POPRReader(username, pwd, True)
	mail.list_mails()
	mail.quit()


if __name__ == '__main__':
	main()