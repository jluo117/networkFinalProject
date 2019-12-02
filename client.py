import socket
import sys
from thread import*
kill = False
def readFromServer():
	while not kill:
		res = sock.recv(1024)
		print(res)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10010)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
try:
	start_new_thread(readFromServer,())
	while 1:
		userInput = raw_input()
		sock.sendall(userInput)
		if userInput == 'q':
			sock.close()
			kill = True
			exit()
finally:
    print >>sys.stderr, 'closing socket'


#fp.clinet

