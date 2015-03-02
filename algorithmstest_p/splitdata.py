
def predata():
	userrate = dict()
	userlist = list()
	with open("../data/ratings.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			userid = int(row[0])
			if userid > 500:
				break
			if int(row[2]) > 3:
				if row[0] not in userlist:
					userlist.append(row[0])
				if row[0] in userrate:
					userrate[row[0]].append(row[1])
				else:
					userrate[row[0]] = list()
					userrate[row[0]].append(row[1])

	testdata = dict()

	for user in userlist:
		testdata[user] = userrate[user].pop()

	with open("traindata.dat", "w") as fw:
		for user in userlist:
			for item in userrate[user]:
				temp = user+"::"+item+"\n"
				fw.write(temp)
	with open("testdata.dat", "w") as fw:
		for user in userlist:
			temp = user+"::"+testdata[user]+"\n"
			fw.write(temp)

def genfeature():
	moviefeature = list()
	with open("../data/movies.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			feature = row[2].split('|')
			for f in feature:
				if f not in moviefeature:
					moviefeature.append(f)

	itemfeature = dict(); userfeature = dict()
	with open("../data/movies.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			item = row[0]
			itemfeature[item] = dict(zip(moviefeature, [0]*len(moviefeature)))
			feature = row[2].split('|')
			for f in feature:
				itemfeature[item][f] = 1

	with open("traindata.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')

			user = row[0];item = row[1]
			if user not in userfeature:
				userfeature[user] = dict(zip(moviefeature, [0]*len(moviefeature)))
			for k in itemfeature[item]:
				if itemfeature[item][k] == 1:
					userfeature[user][k] = userfeature[user][k] + 1

	with open("itemfeature.dat", "w") as fw:
		for i in itemfeature:
			temp = i+","
			templist = list()
			for f in moviefeature:
				templist.append(str(itemfeature[i][f]))
			temp = temp + ','.join(templist) + "\n"
			fw.write(temp)

	with open("userfeature.dat", "w") as fw:
		for i in userfeature:
			temp = i+","
			templist = list()
			tempsum = list()
			for f in moviefeature:
				#if userfeature[i][f] != 0:
				#	tempnum = str(math.log(float(userfeature[i][f])) / math.log(10))
				#else:
				#	tempnum = "0"
				tempnum = str(userfeature[i][f])
				templist.append(tempnum)
				tempsum.append(userfeature[i][f])
			temp = temp + str(sum(tempsum)) +","+','.join(templist) + "\n"
			fw.write(temp)

if __name__ == "__main__":
	genfeature()