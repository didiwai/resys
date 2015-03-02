
def createMatrix():
	userfeat = dict()
	with open("train.dat", "r") as f:
		for row in f.readlines():
			row = row.strip().split('::')
			user = int(row[0]); item = int(row[1])
			if int(row[2]) > 3:
				if user not in userfeat:
					userfeat[user] = [0]*3952
				userfeat[user][item-1] = 1
	with open("usermatrix.dat", "w") as fw:
		for i in range(1, 201):
			temp = ','.join(str(x) for x in userfeat[i])+"\n"
			fw.write(temp)


if __name__ == "__main__":
	createMatrix()