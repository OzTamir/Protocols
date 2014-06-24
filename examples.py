from src.FTP.ftp import FTPClient
from src.Email.pop3 import POPClient
import getpass

DEBUG = False

def ftp_demo():
	global DEBUG
	''' Short example: Download the index file from a website '''
	port = 21
	# Prompt the user to enter his login details
	server = raw_input('Please enter server address: ')
	# Create a FTP client
	ftp = FTPClient(server, port, DEBUG)
	# Get logins from user
	username = raw_input('Please Enter Your Username: ')
	pwd = getpass.getpass('Please Enter Password: ')
	# Login
	ftp.login(username, pwd)
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

def POP3_demo():
	global DEBUG
	''' Short example: Display a list of messages in your inbox '''
	# Prompt the user for server details
	server = raw_input('Please enter the POP3 server: ')
	port = int(raw_input("Please enter the server's POP3 port: "))
	# Create a POP3 client
	mail = POPClient(server, port, DEBUG)
	# Prompt the user for login details
	username = raw_input('Please Enter Your Username: ')
	pwd = getpass.getpass('Please Enter Password: ')
	mail.login(username, pwd)
	# List the unread mails
	mail.list_mails()
	# Quit
	mail.quit()
