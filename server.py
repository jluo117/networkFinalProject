import socket
import sys
from thread import *
from twitter import *
class ConnectionInfo:
	def __init__ (self,connection,client):
		self.Connection = connection
		self.Client = client
	def sengMsg(self,msg):
		print("sending")
		self.Connection.sendto(msg,self.Client)
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tw = twitter()
#Bind the socket to the port
server_address = ('localhost', 10010)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(10)
signIn = {}
clients = {}
def printMenu(connection,client_address):
	connection.sendto("\n---MAIN MENU---\n1: View Offline Messages\n2: Show Subscriptions\n3: Add a Subscription\n4: Delete a Subscription\n5: Create a Tweet\n6: Find messages using a Tag\n--------------------\n",client_address)


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
				newConnection = ConnectionInfo(connection,client_address)
				signIn[curUser] = newConnection
				count = 0
				userTable = tw.table
				#start_new_thread(updateThread,(connection,client_address,curUser))
			continue
		printMenu(connection,client_address)
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
			posSubs = tw.showAllSub()
			connection.sendto(str(posSubs) + '\n',client_address)
			connection.sendto("enter the desire sub\n",client_address)
			sub = connection.recv(1024)
			if sub == "back":
				continue
			tw.addNewSub(curUser,sub)
		elif data == "4":
			userSubs = tw.showSub(curUser)
			connection.sendto("select the desire sub to delete\n",client_address)
			result = tw.showSub(curUser)
			connection.sendto(str(result) + '\n',client_address)
			if sub == "back":
				continue
			delSub = connection.recv(1024)
			tw.delSub(curUser,delSub)
		elif data == "5":
			connection.sendto("enter your tag\n",client_address)
			sub = connection.recv(1024)
			if sub == "back":
				continue
			connection.sendto("enter your msg\n",client_address)
			msg = connection.recv(1024)
			while len(msg) > 140:
				connection.sendto("140 char max\n",client_address)
				msg = connection.recv(1024)
			sendAry = tw.addMsg(sub,msg)
			users = tw.table
			print(users)
			for user in users:
				curAry = users[user]
				trueTags = []
				for tag in curAry:
					trueTags.append(tag.tag)
				if sub in trueTags:
					if user in signIn:
						print(user)
						sendStuff = signIn[user]
						sendStuff.sengMsg(msg)


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
			del signIn[curUser]
			break
        finally:
            
            connection.close()



while True:
    connection, client_address = sock.accept()
    print 'Connected to ' + client_address[0] + ':' + str(client_address[1])
    clients[connection] = client_address
    start_new_thread(clientthread, (connection,client_address,))
sock.close()
#fp_server



