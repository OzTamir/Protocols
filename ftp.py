from ProtocolBase import ProtocolBase
import getpass
import socket
import ssl
from math import log

class FTPPassiveClient:
	''' A class to handle the connection to the server on passive mode '''
	def __init__(self):
		self.enabled = False
		self.addr = ''
		self.port = 0
		self.connected = False
		self.sock = None

	def enable(self, data):
		''' Enable passive mode '''
		self.enabled = True
		# Initialize the IP address to which the server is listening
		self.init_addr(data)

	def connect(self):
		''' Connect to the server on the listining port '''
		if self.addr == '' or port == 0:
			print 'ERROR: PASV Mode not enabled'
			return
		if self.connected:
			return
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.addr, self.port))
	
	def init_addr(self, data):
		''' Get the IP at which the server is waiting for clients '''
		# The format of the data is '227 Entering Passive Mode (IP,IP,IP,IP,PORT,PORT)'
		addr = data[:-2].split('(')[1].split(',')
		self.addr = '.'.join(addr[:4])
		# Get the port
		self.port = int(addr[4]) * 256
		self.port += int(addr[5])
		return

	def get_passive_addr(self):
		''' This is mostly a debug feature ; print the address at which the server is listening '''
		return self.addr + ':' + str(self.port)

	def ftp_read(self, size):
		''' When entering PASV mode, the FTP server wait for a client to connect and read the output from the last commands '''
		if self.addr == '' or port == 0:
			print 'ERROR: PASV Mode not enabled'
			return
		data = ''
		overflow = -1
		loop_cnt = 8
		if size > 4096:
			overflow = size % 4096
			# We use max to avoid multiply by zero
			loop_cnt *= max(size // 4096, 1)
			size = 4096
		# Each char is 8-bit long since we're dealing with ASCII encoding
		# Therfor, we need to read the filesize * 8 to read the entire file
		recived = 0
		total = loop_cnt * (size + overflow)
		for i in range(loop_cnt):
			data += self.sock.recv(size)
			# Print download progress
			recived += size
			print 'Download at ', int(round((recived * 100.0) / total)), '%'
		
		if overflow != -1:
			data += self.sock.recv(overflow)
			# Print download progress
			recived += overflow
			print 'Download at ', int(round((recived * 100.0) / total)), '%'
		print 'Done!'
		return data

	def close(self):
		''' Close the connection to the server '''
		self.sock.close()

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
		# '331' code indicate the response to the USER command, meaning we've read all we've needed to
		while data[:3] != '331':
			data = self.read()
		# Send the password
		self.send('PASS', self.password, True)
		return

	def download_file(self, filename):
		''' Download a file from the server '''
		# Make sure that passive mode is enabled
		if not self.pasv.enabled:
			self.go_pasv()
		# Connect to the server listening port
		self.pasv.connect()
		# Retrive the requested file's size (bytes)
		self.send('SIZE', filename)
		res = self.read().split(' ')
		# '550' means the file cannot be found
		if res[0] == '550':
			print "ERROR: Can't find file"
			return
		# Else, the response's data will be the file size
		file_size = int(res[1])
		# Inform the user of what we're currently doing
		print 'Downloading ', filename, '(Size: ', file_size, ')'
		# Tell the server what file we want to download
		self.send('RETR', filename)
		# Read the file from the server
		file_data = self.pasv.ftp_read(file_size)
		# Write the file to a file
		with open(filename, 'w') as newfile:
			newfile.write(file_data)

	def go_pasv(self):
		''' Enable passive mode '''
		# If it's already enabled no need to enable it again
		if self.pasv.enabled:
			return
		# Ask the server to enable it for us
		self.send('PASV', '', True)
		# Get the address at which the server wait for connection
		data = self.read()
		# Set the passive client to this address
		self.pasv.enable(data)
		# If debugging is enabled, print the address to which the server listen
		if self.debug:
			print self.pasv.get_passive_addr()

	def change_dir(self, target_dir):
		''' Change the current working directory '''
		self.send('CWD', target_dir, True)

	def quit(self):
		''' Quit the session '''
		self.pasv.close()
		self.send('QUIT')


def main():
	''' Short example: Download the index file from a website '''
	port = 21
	# Prompt the user to enter his login details
	server = raw_input('Please enter server address: ')
	username = raw_input('Please Enter Your Username: ')
	pwd = getpass.getpass('Please Enter Password: ')
	ftp = FTPClient(username, pwd, True)
	# Move to the public_html directory
	ftp.change_dir('public_html')
	# Enable passive mode
	ftp.go_pasv()
	# Set the type to ascii
	ftp.send('TYPE', 'A', True)
	# Download the index file
	ftp.download_file('index.html')
	# Quit
	ftp.quit()

if __name__ == '__main__':
	main()