import operator
import time
import math
from itertools import izip

def mixPathAlgorithm(user, useroutnode, itemoutnode, sim, testitemlist):
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

	#rank_sorted = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
	
	newrank = dict(); itemratedict = dict()
	for key in testitemlist:
		key = key.split('::')
		item = int(key[0])
		itemratedict[item] = int(key[1])
		if item in rank:
			newrank[item] = rank[item]
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


def similarityBetweenTwoNode(userlist, itemlist, useritemsim, useroutdegree, itemoutdegree, flag):
	sim = dict()
	for u in userlist:
		for i in itemlist:
			index_1 = "u_"+str(u)+"::"+"i_"+str(i)
			index_2 = "i_"+str(i)+"::"+"u_"+str(u)
			#base
			if flag == 1:
				if useritemsim[index_1] == 0:
					sim[index_1] = 0
					sim[index_2] = 0
				else:
					sim[index_1] = useritemsim[index_1]
					sim[index_2] = useritemsim[index_1]
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



def recommendTopNItemNoTime(flag):

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

	rating = dict();userlist = list();itemlist = list()
	useroutdegree = dict();itemoutdegree = dict()
	userconnectnode = dict();itemconnectnode = dict()

	with open("train.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')

			user = int(row[0]);item = int(row[1])
			if int(row[2]) > 3:
				if user not in userlist:
					userlist.append(user)
				if item not in itemlist:
					itemlist.append(item)

				createoutdegree(user, useroutdegree)
				createoutdegree(item, itemoutdegree)
				createnodeconnectnode(user, item, userconnectnode)
				createnodeconnectnode(item, user, itemconnectnode)

			#ratekey = row[0]+"::"+row[1]
			#rating[ratekey] = int(row[2])

	testdatadict = dict()
	with open("test.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			#tempkey = "u_"+row[0]+"::"+"i_"+row[1]
			#testdatadict[tempkey] = int(row[2])
			user = int(row[0])
			if user not in testdatadict:
				testdatadict[user] = list()
			temp = row[1]+"::"+row[2]
			testdatadict[user].append(temp)

	with open("top10RecommendNoTimeBasedAlgriothmOnlySim.txt", "w") as fw:
		fw.write("NDCG@1\tNDCG@2\tNDCG@3\tNDCG@4\tNDCG@5\n")

		sim = similarityBetweenTwoNode(userlist, itemlist, useritemsim, useroutdegree, itemoutdegree, flag)
		total = 0
		idcg_all = dict(zip(range(1,6), [0.0]*5))
		for user in userlist:
			if user not in testdatadict:
				continue
			testitemlist = testdatadict[user]
			total = total + 1
			ndcg_k = mixPathAlgorithm(user, userconnectnode, itemconnectnode, sim, testitemlist)

			for t in ndcg_k:
				idcg_all[t] = idcg_all[t] + ndcg_k[t]
		temp_2 = list()
		for k in idcg_all:
			print idcg_all[k]
			temp_2.append(str(idcg_all[k]/total))
		tempwirte = "\t".join(temp_2)+"\n"
		fw.write(tempwirte)

if __name__ == "__main__":
	recommendTopNItemNoTime(1)
