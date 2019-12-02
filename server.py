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
        res = tw.printLastMessage(User)
        newStr = ""
        for val in res:
                newStr += val + '\n'
        print(newStr)
        if newStr == "":
                return "Empty"
        return newStr
def updateThread(connection,client_address,user):
	while 1:
		result = printLastMessage(user)
		if result != "Empty":
			 connection.sendto(result,client_address)
def clientthread(connection,client_address):
    #connection.send("Welcome to Twitter.\n \n \n MAIN MENU:\n ")
    while True:
        # Wait for a connection
        #print >>sys.stderr, 'waiting for a connection'
        #connection, client_address = sock.accept()
 
        try:
	    offLineMsg = {}
            print >>sys.stderr, 'connection from', client_address
            # Receive the data in small chunks and retransmit it
            login = False
	    curUser = "NULL"
	    while True:
		if not login:
			connection.sendto("insert username",client_address)
			userName = connection.recv(1024)
			connection.sendto("insert password",client_address)
			password = connection.recv(1024)
			if tw.login(userName,password):
				curUser = userName
				login = True
				if curUser == "admin":
					continue
				connection.sendto("Welcome " + curUser + '\n',client_address)
				offLineMsg = tw.offLineMsg(curUser)
				tw.userSignOn(curUser,connection,client_address)
				count = 0
				#start_new_thread(updateThread,(connection,client_address,curUser))
				for tags in offLineMsg:
					count += len(offLineMsg[tags])
				connection.sendto("You have " + str(count) + " messages\n",client_address)
			continue
		connection.sendto("waiting for input",client_address)
		data = connection.recv(1024)	
		if data == "1":
			connection.sendto("Do you want ALL offline msgs or just a sub",client_address)
			choice = connection.recv(1024)
			if choice == "ALL":
				connection.sendto(str(offLineMsg) + '\n',client_address)
			else:
				if choice not in offLineMsg:
					connection.sendto("KeyError\n",client_address)
				else:
					connection.sendto(str(offLineMsg[choice]) + '\n',client_address)
		elif data == "2":
			result = tw.showSub(curUser)
			connection.sendto("you are sub to the following\n",client_address)
			connection.sendto(str(result),client_address)
		elif data == "3":
			connection.sendto("enter the desire sub\n",client_address)
			sub = connection.recv(1024)
			tw.addNewSub(curUser,sub)
		elif data == "4":
			userSubs = tw.showSub(curUser)
			connection.sendto("select the desire sub to delete\n",client_address)
			result = tw.showSub(curUser)
			connection.sendto(str(result) + '\n',client_address)
			delSub = connection.recv(1024)
			tw.delSub(curUser,delSub)
		elif data == "5":
			connection.sendto("enter your tag\n",client_address)
			sub = connection.recv(1024)
			connection.sendto("enter your msg\n",client_address)
			msg = connection.recv(1024)
			while len(msg) > 140:
				connection.sendto("140 char max\n",client_address)
				msg = connection.recv(1024)
			tw.addMsg(sub,msg)
		elif data == "6":
			connection.sendto("enter a tag to lookup\n",client_address)
			lookup = connection.recv(1024)
			res = tw.hashSearch(lookup)
			if res == None:
				connection.sendto("Sub not found\n",client_address)
			else:
				connection.sendto(str(res) + '\n',client_address)
		elif data == "messagecount" and curUser == "admin":
			count = tw.msgCount()
			connection.sendto(str(count) + " message\n",client_address)

		elif data == "q":
			tw.userLogOut(curUser)
			break
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


