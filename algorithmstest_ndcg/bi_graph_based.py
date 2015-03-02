import operator
import time
import math
from itertools import izip

'''
def simBetweenTwoNode(a_node, b_node, nodeoutdegree, flag, p):
	result = 0.0
	temp_node_out = 1.0 / (pow(nodeoutdegree[a_node], p))
	#no time feature

	#base algorithm useing only out|node| 
	if flag == 1:
		result = temp_node_out
	#use out|node| * similiarity between two node
	elif flag == 2:
		sim = similiarityBetweenTwoNode(a_node, b_node)
	return result
'''

def mixPathAlgorithm(node, out_node, sim, testitemlist):
	Q = list();V = list()
	Q.append(node);distance = dict(); rank = dict()
	distance[node] = 0;rank[node] = 1

	while Q:
		v = Q.pop(0)
		if v in V:
			continue
		if v in distance and distance[v] > 3:
			break
		V.append(v)
		for vn in out_node[v]:
			if vn not in V:
				distance[vn] = distance[v] + 1
				Q.append(vn)
			if distance[v] < distance[vn]:
				tempsim = sim[v+"::"+vn]
				if v not in rank:
					rank[v] = 1
				tempres = rank[v]*tempsim
				if vn in rank:
					rank[vn] = rank[vn] + tempres
				else:
					rank[vn] = 1 + tempres

	#rank_sorted = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
	
	newrank = dict(); itemratedict = dict()
	for key in testitemlist:
		key = key.split('::')
		item = int(key[0])
		itemratedict[item] = int(key[1])
		itemname = "i_"+str(item)
		if itemname in rank:
			newrank[item] = rank[itemname]
	rank_sorted = sorted(newrank.items(), key=operator.itemgetter(1), reverse=True)

	ndcg_k = dict()
	for N in range(1, 6):
		dcg = 0.0; num = 1; idealrank = list()
		for i in rank_sorted:
			temp = int(i[0])
			idealrank.append(itemratedict[temp])
			if num <= N:
				dcg = dcg + float(2**itemratedict[temp] - 1) / (float(math.log(1+num))/math.log(2))
				num = num + 1
		idcg = 0.0;num = 1
		idealrank.sort(reverse=True)
		for t in idealrank:
			if num > N:
				break
			idcg = idcg + float(2**t - 1) / (float(math.log(1+num))/math.log(2))
			num = num + 1

		ndcg_k[N] = dcg / idcg
	return ndcg_k

def createoutdegree(node, outdegree):
	if node in outdegree:
		outdegree[node] = outdegree[node] + 1
	else:
		outdegree[node] = 1

def createnodeconnectnode(node1, node2, connectdict):
	if node1 not in connectdict:
		connectdict[node1] = list()
	connectdict[node1].append(node2)

def similarityBetweenTwoNode(userlist, itemlist, useritemsim, nodeoutdegree, flag, p):
	sim = dict()
	for u in userlist:
		for i in itemlist:
			index_1 = u+"::"+i
			index_2 = i+"::"+u
			#base
			if flag == 1:
				if useritemsim[index_1] == 0:
					result = 1.0 / (pow(nodeoutdegree[u], p))
					sim[index_1] = result

					result = 1.0 / (pow(nodeoutdegree[i], p))
					sim[index_2] = result
				else:
					result = 1.0 / (pow(nodeoutdegree[u], p))
					result_1 = result * useritemsim[index_1]
					sim[index_1] = result_1

					result = 1.0 / (pow(nodeoutdegree[i], p))
					result_2 = result * useritemsim[index_1]
					sim[index_2] = result_2

	return sim
'''
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
	return useritemsim
'''
def userSimItem():
	useritemsim = dict()
	with open("downleft.txt", "r") as f:
		line = 1
		for row in f.readlines():
			row = row.strip().split(',')
			newrow = [float(x) for x in row]
			maxnumber = max(newrow)
			for r in range(0, 3952):
				index = "u_"+str(line)+"::i_"+str(r+1)
				useritemsim[index] = newrow[r] / float(maxnumber)
			line = line + 1
	return useritemsim
def recommendTopNItemNoTime(N, flag):
	rating = dict();userlist = list();itemlist = list()
	nodeoutdegree = dict();nodeconnectnode = dict()

	with open("train.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			if int(row[2]) > 3:
				user = "u_"+row[0];item = "i_"+row[1]
				if user not in userlist:
					userlist.append(user)
				if item not in itemlist:
					itemlist.append(item)

				createoutdegree(user, nodeoutdegree)
				createoutdegree(item, nodeoutdegree)
				createnodeconnectnode(user, item, nodeconnectnode)
				createnodeconnectnode(item, user, nodeconnectnode)
	'''
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
	'''
	useritemsim = userSimItem()

	testdatadict = dict()
	with open("test.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			user = "u_"+row[0]
			if user not in testdatadict:
				testdatadict[user] = list()
			temp = row[1]+"::"+row[2]
			testdatadict[user].append(temp)

	#with open("test.txt", "w") as fw:
	sim = similarityBetweenTwoNode(userlist, itemlist, useritemsim, nodeoutdegree, 1, 0.1)
	total = 0
	idcg_all = dict(zip(range(1,6), [0.0]*5))
	for user in userlist:
		if user not in testdatadict:
			continue
		testitemlist = testdatadict[user]
		total = total + 1
		print "total: "+str(total)
		ndcg_k = mixPathAlgorithm(user, nodeconnectnode, sim, testitemlist)
		for t in ndcg_k:
			idcg_all[t] = idcg_all[t] + ndcg_k[t]
	temp_2 = list()
	for k in idcg_all:
		print idcg_all[k]


if __name__ == "__main__":
	recommendTopNItemNoTime(10, 1)
