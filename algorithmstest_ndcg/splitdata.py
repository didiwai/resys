from sklearn.cross_validation import train_test_split
import numpy as np


def splitDataRandom():
	temparray = list()
	with open("../data/ratings.dat", 'r') as f:
		for row in f.readlines():
			row =  row.strip()
			row =  row.split('::')
			if int(row[0]) > 200:
				break
			temparray.append([row[0], row[1], row[2]])

	myarray = np.asarray(temparray)
	a_train, a_test= train_test_split(myarray, test_size=0.5, random_state=42)
	with open('train.dat', 'w') as f:
		for row in a_train:
			temp = row[0] + "::" + row[1] + "::" + row[2] + '\n'
			f.write(temp)
	with open('test.dat', 'w') as f:
		for row in a_test:
			temp = row[0] + "::" + row[1] + "::" + row[2] +'\n'
			f.write(temp)

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

	with open("train.dat", "r") as f:
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