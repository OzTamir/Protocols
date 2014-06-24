from ..ProtocolBase import ProtocolBase
import getpass
import socket
import ssl

def print_seperetor():
	print '---------------------'

class POPClient(ProtocolBase):
	''' A POP3-Based Email reader with SSL '''
	def __init__(self, server, port, debug=False):
		''' Open socket and login to the server '''
		ProtocolBase.__init__(self, server, port, debug)

	def login(self, user, pwd):
		''' Login to the server '''
		self.username = user
		self.password = pwd
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