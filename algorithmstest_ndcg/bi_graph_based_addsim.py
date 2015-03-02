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
							rank[last_item] = 1 + tempres_2 * sim[tempname_3]
						else:
							rank[last_item] = rank[last_item] + tempres_2 * sim[tempname_3]

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


def similarityBetweenTwoNode(userlist, itemlist, useritemsim, useroutdegree, itemoutdegree, flag, p):
	sim = dict()
	for u in userlist:
		for i in itemlist:
			index_1 = "u_"+str(u)+"::"+"i_"+str(i)
			index_2 = "i_"+str(i)+"::"+"u_"+str(u)
			#base
			if flag == 1:
				if useritemsim[index_1] == 0:
					result = 1.0 / (pow(useroutdegree[u], p))
					sim[index_1] = result

					result = 1.0 / (pow(itemoutdegree[i], p))
					sim[index_2] = result
				else:
					result = 1.0 / (pow(useroutdegree[u], p))
					result_1 = result * useritemsim[index_1]
					sim[index_1] = result_1

					result = 1.0 / (pow(itemoutdegree[i], p))
					result_2 = result * useritemsim[index_1]
					sim[index_2] = result_2
	return sim

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

	useritemsim = userSimItem()

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

	with open("top10RecommendNoTimeBasedAlgriothmAddSim_p.txt", "w") as fw:
		fw.write("p\tNDCG@1\tNDCG@2\tNDCG@3\tNDCG@4\tNDCG@5\n")

		plist = [float(x)/100 for x in range(100, 160, 10)]
		for p in plist:

			sim = similarityBetweenTwoNode(userlist, itemlist, useritemsim, useroutdegree, itemoutdegree, flag, p)
			total = 0
			idcg_all = dict(zip(range(1,6), [0.0]*5))
			print "p: "+str(p)
			for user in userlist:
				if user not in testdatadict:
					continue
				testitemlist = testdatadict[user]
				total = total + 1
				#print "p: "+str(p)+"  total: "+str(total)
				#start_time = time.time()
				ndcg_k = mixPathAlgorithm(user, userconnectnode, itemconnectnode, sim, testitemlist)

				for t in ndcg_k:
					idcg_all[t] = idcg_all[t] + ndcg_k[t]
				#end_time = time.time() - start_time
				#print "time is: " + str(end_time)
			temp_2 = list()
			for k in idcg_all:
				print idcg_all[k]
				temp_2.append(str(idcg_all[k]/total))
			tempwirte = str(p)+"\t"+"\t".join(temp_2)+"\n"
			fw.write(tempwirte)
			#fw.write(str(p)+"\tNDCG@"+str(k)+"\t"+str(idcg_all[k]/total)+"\n")

if __name__ == "__main__":
	recommendTopNItemNoTime(1)
