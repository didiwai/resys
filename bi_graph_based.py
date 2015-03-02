import operator
import time

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

def mixPathAlgorithm(node, out_node, sim):
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

	rank_sorted = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
	return rank_sorted

def createoutdegree(node, outdegree):
	if node in outdegree:
		outdegree[node] = outdegree[node] + 1
	else:
		outdegree[node] = 1

def createnodeconnectnode(node1, node2, connectdict):
	if node1 not in connectdict:
		connectdict[node1] = list()
	connectdict[node1].append(node2)

def similarityBetweenTwoNode(userlist, itemlist, nodeoutdegree, flag, p):
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
	return sim


def recommendTopNItemNoTime(N, flag):
	rating = dict();userlist = list();itemlist = list()
	nodeoutdegree = dict();nodeconnectnode = dict()

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

	sim = similarityBetweenTwoNode(userlist, itemlist, nodeoutdegree, 1, 0.1)

	total = 0;tempnumber = 0
	with open("top10RecommendNoTimeBasedAlgriothm_p.txt", "w") as fw:
		fw.write("p\thitratio\n")
		for user in userlist:
			total = total + 1
			print "total:"+str(total)

			start_time = time.time()
			testdata = int(nodeconnectnode[user].pop().split('_')[1])
			recommendturple = mixPathAlgorithm(user, nodeconnectnode, sim)
			j = 1
			rank_list = list()
			for i in recommendturple:
				print i
				if j > N:
					break
				temp = int(i[0].split('_')[1])
				rank_list.append(temp)
				j = j + 1
			if testdata in rank_list:
				tempnumber = tempnumber + 1
			end_time = time.time() - start_time
			print "time is:" + str(end_time)
		#hitratio = float(tempnumber[p]) / total
		#fw.write(str(p)+"\t"+str(hitratio)+"\n")

if __name__ == "__main__":
	recommendTopNItemNoTime(10, 1)
