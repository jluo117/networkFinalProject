import socket
import sys
from thread import*
kill = False
def readFromServer():
	while not kill:
		res = sock.recv(1024)
		print('\n' + res)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10009)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
try:
    LogIn = False
    while not LogIn: 
    	print('Welcome (back) to Twitter!')
    	login = raw_input("Enter username: ")
    	password = raw_input("Enter password: ")
    	logininfo = "login " + login + " " + password
    	sock.sendall(logininfo)    
    	res = sock.recv(1024)
	if res != "0":
		logIn = True
		print("Log in Good")
		break
    	else:
		print("Log in Fail")
    start_new_thread(readFromServer,())
    while True:
        # Send data
        message = raw_input("Input: ")
	if(message == "Quit" or message == 'quit'):
	    kill = True
	    sock.close()
	    exit()
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()


#fp.clinet

