import operator
import math
from itertools import izip


def mixPathAlgorithm(user, out_node, sim):
	rank = dict();rank[user] = 1

	#one loop
	for u_next_i in out_node[user]:
		tempname_1 = user+"::"+u_next_i
		tempres_1 = 1 + sim[tempname_1]
		#two loop
		for i_next_u in out_node[u_next_i]:
			if i_next_u != user:
				tempname_2 = u_next_i+"::"+i_next_u
				tempres_2 = 1 + tempres_1 * sim[tempname_2]
				#three loop
				for last_item in out_node[i_next_u]:
					if last_item != u_next_i:
						tempname_3 = i_next_u+"::"+last_item
						if last_item not in rank:
							rank[last_item] = 1 + tempres_2*sim[tempname_3]
						else:
							rank[last_item] = rank[last_item] + tempres_2*sim[tempname_3]

	rank_sorted = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
	return rank_sorted


def similarityBetweenTwoNode(userlist, itemlist, useritemsim, nodeoutdegree, flag, p):
	sim = dict()
	for u in userlist:
		for i in itemlist:
			index_1 = u+"::"+i
			index_2 = i+"::"+u
			#base
			if flag == 1:
				result = 1.0 / (pow(nodeoutdegree[u], p))
				sim[index_1] = result

				result = 1.0 / (pow(nodeoutdegree[i], p))
				sim[index_2] = result
			#add sim
			if flag == 2:
				if useritemsim[index_1] == 0:
					result = 1.0 / (pow(nodeoutdegree[u], p))
					sim[index_1] = result

					result = 1.0 / (pow(nodeoutdegree[i], p))
					sim[index_2] = result
				else:
					result = 1.0 / (pow(nodeoutdegree[u], p))
					result = result * useritemsim[index_1]
					sim[index_1] = result

					result = 1.0 / (pow(nodeoutdegree[i], p))
					result = result * useritemsim[index_1]
					sim[index_2] = result
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
			index = u+"::"+i
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

def recommendTopNItemNoTime(N, flag):
	rating = dict();userlist = list();itemlist = list()
	nodeoutdegree = dict();nodeconnectnode = dict()
	'''
	moviefeature = list()
	with open("data/movies.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			feature = row[2].split('|')
			for f in feature:
				if f not in moviefeature:
					moviefeature.append(f)

	itemfeature = dict(); userfeature = dict()
	with open("data/movies.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			item = "i_"+row[0]
			itemfeature[item] = dict(zip(moviefeature, [0]*len(moviefeature)))
			feature = row[2].split('|')
			for f in feature:
				itemfeature[item][f] = 1

	with open("data/ratings.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			if int(row[2]) > 3:
				user = "u_"+row[0];item = "i_"+row[1]
				if user not in userfeature:
					userfeature[user] = dict(zip(moviefeature, [0]*len(moviefeature)))
				for k in itemfeature[item]:
					if itemfeature[item][k] == 1:
						userfeature[user][k] = userfeature[user][k] + 1

	with open("data/itemfeature.dat", "w") as fw:
		for i in itemfeature:
			temp = i+","
			templist = list()
			for f in moviefeature:
				templist.append(str(itemfeature[i][f]))
			temp = temp + ','.join(templist) + "\n"
			fw.write(temp)

	with open("data/userfeature.dat", "w") as fw:
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

	'''
	userfeature = dict();itemfeature = dict()
	with open("data/itemfeature.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split(',')
			itemfeature[row[0]] = [int(x) for x in row[1:]]
	with open("data/userfeature.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split(',')
			sumnum = int(row[1])
			userfeature[row[0]] = [float(x)/sumnum for x in row[2:]]

	useritemsim = userSimItem(userfeature, itemfeature)

	with open("data/ratings.dat", "r") as f:
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

				ratekey = row[0]+"::"+row[1]
				rating[ratekey] = int(row[2])


	with open("top10RecommendNoTimeBasedAlgriothm_p.txt", "w") as fw:
		fw.write("p\thitratio\n")

		plist = [float(x)/100 for x in range(10, 160, 10)]
		for p in plist:
			sim = similarityBetweenTwoNode(userlist, itemlist, useritemsim,nodeoutdegree, flag, p)
			total = 0;tempnumber = 0
			for user in userlist:
				total = total + 1
				print "p: "+str(p)+"total: "+str(total)
				testdata = int(nodeconnectnode[user].pop().split('_')[1])
				recommenditem = mixPathAlgorithm(user, nodeconnectnode, sim)
				j = 1
				rank_list = list()
				for i in recommenditem:
					if j > N:
						break
					temp = int(i[0].split('_')[1])
					rank_list.append(temp)
					j = j + 1
				if testdata in rank_list:
					tempnumber = tempnumber + 1
			
			hitratio = float(tempnumber) / total
			fw.write(str(p)+"\t"+str(hitratio)+"\n")


if __name__ == "__main__":
	recommendTopNItemNoTime(10, 2)
