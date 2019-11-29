import socket
import sys
from thread import *
from twitter import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tw = twitter()
#Bind the socket to the port
server_address = ('localhost', 10009)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(10)

clients = set()

def printLastMessage(User):
        print(User)
        res = tw.printLastMessage(User)
        newStr = ""
        for val in res:
                newStr += val + '\n'
        print(newStr)
        if newStr == "":
                return "Empty"
        return newStr
def clientthread(connection,client_address):
    #connection.send("Welcome to Twitter.\n \n \n MAIN MENU:\n ")
    while True:
        # Wait for a connection
        #print >>sys.stderr, 'waiting for a connection'
        #connection, client_address = sock.accept()
 
        try:
            print >>sys.stderr, 'connection from', client_address
            # Receive the data in small chunks and retransmit it
            login = False
	    curUser = "NULL"
	    while True:
		data = connection.recv(1024)
		if not login:
    	        	splitData = data.split()
			print(splitData)
                	if splitData[0] == 'login':
				res = tw.login(splitData[1],splitData[2])
				print(res)
				if not res:
					connection.sendto("0",client_address)
					connection.sendto("Please enter username and password again",client_address)
					continue

				else:
					curUser = splitData[1]
					connection.sendto("1",client_address)
					login = True
					print("log in good")
			continue
		
		print(data)
		if data == "1":
                        result = printLastMessage(curUser)
                        connection.sendto(result,client_address)
                        print("sent")


        finally:
            #clients.remove(connection)
            connection.close()



while True:
    connection, client_address = sock.accept()
    print 'Connected to ' + client_address[0] + ':' + str(client_address[1])
    clients.add(connection)
    start_new_thread(clientthread, (connection,client_address,))
sock.close()
#fp_server


