import operator
import time

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


def similarityBetweenTwoNode(userlist, itemlist, useroutdegree, itemoutdegree, flag, p):
	sim = dict()
	for u in userlist:
		for i in itemlist:
			index_1 = "u_"+str(u)+"::"+"i_"+str(i)
			index_2 = "i_"+str(i)+"::"+"u_"+str(u)
			#base
			if flag == 1:
				result = 1.0 / (pow(useroutdegree[u], p))
				sim[index_1] = result

				result = 1.0 / (pow(itemoutdegree[i], p))
				sim[index_2] = result
	return sim


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

			#ratekey = row[0]+"::"+row[1]
			#rating[ratekey] = int(row[2])

	testdatadict = dict()
	with open("testdata.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			user = int(row[0])
			if user not in testdatadict:
				testdatadict[user] = int(row[1])
			else:
				print "error test data"

	with open("top10RecommendNoTimeBasedAlgriothm_p.txt", "w") as fw:
		fw.write("p\thitratio\n")

		plist = [float(x)/100 for x in range(10, 160, 10)]
		for p in plist:

			sim = similarityBetweenTwoNode(userlist, itemlist, useroutdegree, itemoutdegree, flag, p)
			total = 0;tempnumber = 0
			print "P "+str(p)
			for user in userlist:
				total = total + 1
				#print "p: "+str(p)+"  total: "+str(total)
				#start_time = time.time()
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
				#end_time = time.time() - start_time
				#print "time is: " + str(end_time)
			hitratio = float(tempnumber) / total
			fw.write(str(p)+"\t"+str(hitratio)+"\n")

if __name__ == "__main__":
	recommendTopNItemNoTime(10, 1)
