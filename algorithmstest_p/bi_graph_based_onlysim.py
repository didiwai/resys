import operator
import math
import time
from itertools import izip


def mixPathAlgorithm(user, useroutnode, itemoutnode, sim):
	rank = dict()

	#one loop
	for u_next_i in useroutnode[user]:
		tempname_1 = "u_"+str(user)+"::"+"i_"+str(u_next_i)
		tempres_1 = sim[tempname_1]
		#two loop
		for i_next_u in itemoutnode[u_next_i]:
			if i_next_u != user:
				tempname_2 = "i_"+str(u_next_i)+"::"+"u_"+str(i_next_u)
				tempres_2 = tempres_1 * sim[tempname_2]
				#three loop
				for last_item in useroutnode[i_next_u]:
					if last_item != u_next_i:
						tempname_3 = "u_"+str(i_next_u)+"::"+"i_"+str(last_item)
						if last_item not in rank:
							rank[last_item] = 1 + tempres_2*sim[tempname_3]
						else:
							rank[last_item] = rank[last_item] + tempres_2*sim[tempname_3]

	rank_sorted = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
	return rank_sorted

def similarityBetweenTwoNode(userlist, itemlist, useritemsim, useroutdegree, itemoutdegree,flag, p):
	sim = dict()
	for u in userlist:
		for i in itemlist:
			index_1 = "u_"+str(u)+"::"+"i_"+str(i)
			index_2 = "i_"+str(i)+"::"+"u_"+str(u)
			#add sim
			if flag == 2:
				if useritemsim[index_1] == 0:
					sim[index_1] = p
					sim[index_2] = p
				else:
					sim[index_1] = useritemsim[index_1]
					sim[index_2] = sim[index_1]
	return sim

def cosine_distance(a, b):
	if len(a) != len(b):
		print "a and b must be same length"
	numerator = sum(tup[0] * tup[1] for tup in izip(a,b))
	denoma = sum(avalue ** 2 for avalue in a)
	denomb = sum(bvalue ** 2 for bvalue in b)
	result = numerator / (math.sqrt(denoma)*math.sqrt(denomb))
	return result

def userSimItem(userfeature, itemfeature):
	useritemsim = dict()
	for u in userfeature:
		for i in itemfeature:
			index = "u_"+str(u)+"::"+"i_"+str(i)
			useritemsim[index] = cosine_distance(userfeature[u], itemfeature[i])
	minelement = 10.0
	for k in useritemsim:
		if useritemsim[k] != 0:
			if minelement > useritemsim[k]:
				minelement = useritemsim[k]
	print minelement
	return useritemsim


def createoutdegree(node, outdegree):
	if node in outdegree:
		outdegree[node] = outdegree[node] + 1
	else:
		outdegree[node] = 1

def createnodeconnectnode(node1, node2, connectdict):
	if node1 not in connectdict:
		connectdict[node1] = list()
	connectdict[node1].append(node2)

def recommendTopNItemNoTime(N, flag):
	rating = dict();userlist = list();itemlist = list()
	useroutdegree = dict();itemoutdegree = dict()
	userconnectnode = dict();itemconnectnode = dict()

	userfeature = dict();itemfeature = dict()
	with open("itemfeature.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split(',')
			itemfeature[int(row[0])] = [int(x) for x in row[1:]]

	with open("userfeature.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split(',')
			sumnum = int(row[1])
			userfeature[int(row[0])] = [float(x)/sumnum for x in row[2:]]

	useritemsim = userSimItem(userfeature, itemfeature)

	with open("traindata.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')

			user = int(row[0]);item = int(row[1])
			if user not in userlist:
				userlist.append(user)
			if item not in itemlist:
				itemlist.append(item)

			createoutdegree(user, useroutdegree)
			createoutdegree(item, itemoutdegree)
			createnodeconnectnode(user, item, userconnectnode)
			createnodeconnectnode(item, user, itemconnectnode)

	testdatadict = dict()
	with open("testdata.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			user = int(row[0])
			if user not in testdatadict:
				testdatadict[user] = int(row[1])
			else:
				print "error test data"

	with open("top10RecommendNoTimeBasedAlgriothmOnlySim.txt", "w") as fw:
		fw.write("p\thitratio\n")

		#plist = [float(x)/100 for x in range(10, 200, 10)]
		#plist = [0.001, 0.002, 0.005, 0.01, 0.1, 1.0]
		plist = [0.0]
		for p in plist:
			sim = similarityBetweenTwoNode(userlist, itemlist, useritemsim, useroutdegree, itemoutdegree, flag, p)
			total = 0;tempnumber = 0
			print "p: "+str(p)
			for user in userlist:
				total = total + 1
				#print "p: "+str(p)+"total: "+str(total)
				testdata = testdatadict[user]
				recommenditem = mixPathAlgorithm(user, userconnectnode, itemconnectnode, sim)
				j = 1
				rank_list = list()
				for i in recommenditem:
					if j > N:
						break
					temp = int(i[0])
					rank_list.append(temp)
					j = j + 1
				if testdata in rank_list:
					tempnumber = tempnumber + 1
			
			hitratio = float(tempnumber) / total
			fw.write(str(p)+"\t"+str(hitratio)+"\n")


if __name__ == "__main__":
	recommendTopNItemNoTime(10, 2)
