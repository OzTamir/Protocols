from ProtocolBase import ProtocolBase
import getpass
import socket
import ssl

server = 
port = 21

class FTPPassiveClient:
	def __init__(self):
		self.enabled = False
		self.addr = ''
		self.port = 0
		self.sock = None

	def enable(self, data):
		self.enabled = True
		self.init_addr(data)

	
	def init_addr(self, data):
		''' Get the IP at which the server is waiting for clients '''
		# The format of the data is '227 Entering Passive Mode (IP,IP,IP,IP,PORT,PORT)'
		addr = data[:-2].split('(')[1].split(',')
		self.addr = '.'.join(addr[:4])
		self.port = int(addr[4]) * 255
		self.port += int(addr[5])
		return

	def ftp_read(self):
		''' When entering PASV mode, the FTP server wait for a client to connect and read the output from the last commands '''
		pass

class FTPClient(ProtocolBase):
	''' A FTP Client '''
	def __init__(self, user, pwd, debug=False):
		global server, port
		ProtocolBase.__init__(self, server, port, debug, False)
		self.username = user
		self.password = pwd
		self.pasv = FTPPassiveClient()
		self.login()

	def login(self):
		''' Login to the server '''
		# Send the username
		self.send('USER', self.username, True)
		# Read all the server's messages
		data = self.read()
		while data[:3] != '331':
			data = self.read()
		# Send the password
		self.send('PASS', self.password, True)
		return

	def go_pasv(self):
		self.send('PASV', '', True)
		data = self.read()
		self.pasv.enable(data)


def main():
	username = raw_input('Please Enter Your Username: ')
	pwd = getpass.getpass('Please Enter Password: ')
	ftp = FTPClient(username, pwd, True)
	ftp.go_pasv()


if __name__ == '__main__':
	main()