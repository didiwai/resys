
userrate = dict()
userlist = list()
with open("data/ratings.dat", "r") as f:
	for row in f.readlines():
		row = row.strip().split('::')
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
