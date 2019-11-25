class userTag:
	def __init__(self,tag):
		self.tag = tag
		self.curIndex = 0
class twitter:
	usersList = {"bob":"123", "root":"root", "page":"larry"}
	table = {"bob":[],"root":[],"page":[]}
	Tags = {}
	
	def login (self,userName,PassWord):
		if userName == "admin" and PassWord == "admin":
			return 2
		if userName not in self.usersList:
			return 0
		if PassWord != self.usersList[userName]:
			return 0
		return 1
	def printLastMessage(self,userName):
		msgToReturn = []
		userTable = self.table[userName]
		for curTag in userTable:
			if curTag.tag in self.Tags:
				for curMsgIndex in range(curTag.curIndex,len(self.Tags[curTag.tag])):
					msgToReturn.append(self.Tags[curTag.tag][curMsgIndex])
				curTag.curIndex = len(self.Tags[curTag.tag])
		return msgToReturn
	def addNewSub(self,userName,sub):
		newSub = userTag(sub)
		self.table[userName].append(newSub)
	def showSub(self,userName):
		subList = []
		for tag in self.table[userName]:
			subList.append(tag.tag)
		return subList
	def delSub(self,userName,sub):
		curUser = self.table[userName]
		for i in range(0,len(curUser)):
			if curUser[i].tag == sub:
				curUser.pop(i)	
				return
	def addMsg(self,sub,msg):
		if len(msg) > 140:
			return False
		if sub in self.Tags:
			self.Tags[sub].append(msg)
		else:
			self.Tags[sub] = [msg]
		return True
	def hashSearch(self,sub):
		if sub not in self.Tags:
			return None
		tagList = self.Tags[sub]
		outPutList = self.Reverse(tagList)
		if len(tagList) < 10:
			return outPutList
		outPut = []
		for i in range(0,10):
			outPut.append(outPutList[i])
		return outPut
	def unreadMsg(self,userName):
		msgTol = self.printLastMessage(userName)
		if msgTol == None:
			return 0
		return len(msgTol)
	def Reverse(self,lst): 
	    return [ele for ele in reversed(lst)] 
