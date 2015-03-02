#include <iostream>
#include <vector>
#include <map>
#include <fstream>
#include <sstream>
#include <string>
#include <queue>
#include <algorithm>

template<typename A, typename B>
std::pair<B,A> flip_pair(const std::pair<A,B> &p)
{
    return std::pair<B,A>(p.second, p.first);
}

template<typename A, typename B>
std::multimap<B,A> flip_map(const std::map<A,B> &src)
{
    std::multimap<B,A> dst;
    std::transform(src.begin(), src.end(), std::inserter(dst, dst.begin()), 
                   flip_pair<A,B>);
    return dst;
}

std::multimap<float, std::string>
 mixPathAlgorithm(std::string node, std::string testdata, std::map<std::string, std::vector<std::string> > out_node, std::map<std::string, int>  nodeoutdegree, int flag, float p) {
	std::queue<std::string> Q;
	std::vector<std::string> V;
	std::map<std::string, int> distance;
	std::map<std::string, float> rank;

	Q.push(node);
	distance[node] = 0;

	while (!Q.empty()) {
		std::string v = Q.front();
		Q.pop();
		if (std::find(V.begin(), V.end(), v) != V.end())
			continue;
		if ((distance.find(v) != distance.end()) && distance[v] > 3)
			break;
		V.push_back(v);
		for (std::vector<std::string>::iterator j = out_node[v].begin(); j != out_node[v].end(); ++j) {
			std::string vn = *j;
			if (std::find(V.begin(), V.end(), vn) == V.end()) {
				distance[vn] = distance[v] + 1;
				Q.push(vn);
			}
			if (distance[v] < distance[vn]) {
				if (rank.find(vn) == rank.end())
					rank[vn] = 1 + rank[v];
				else
					rank[vn] = rank[vn] + rank[v];
			}
		}
	}

	std::multimap<float, std::string> reverseTest = flip_map(rank);
	return reverseTest;

}

int main() {
	std::vector<std::string> userlist;
	std::map<std::string, int> nodeoutdegree;
	std::map<std::string, std::vector<std::string> > nodeconnectnode;

	FILE *fp = fopen("data/ratings.dat", "r");
	int x, y, z, t;

	while (fscanf(fp, "%d::%d::%d::%d", &x, &y, &z, &t) == 4) {
		//std::cout << x << "\n";
		if (z > 3) {
			std::string user("u_");
			std::string item("i_");
			user += std::to_string(x);
			item += std::to_string(y);

			if (std::find(userlist.begin(), userlist.end(), user) == userlist.end())
				userlist.push_back(user);

			if (nodeoutdegree.find(user) == nodeoutdegree.end())
				nodeoutdegree[user] = 1;
			else
				nodeoutdegree[user] = nodeoutdegree[user] + 1;
			if (nodeoutdegree.find(item) == nodeoutdegree.end())
				nodeoutdegree[item] = 1;
			else
				nodeoutdegree[item] = nodeoutdegree[item] + 1;

			if (nodeconnectnode.find(user) == nodeconnectnode.end())
				nodeconnectnode[user].push_back(item);
			else
				if (std::find(nodeconnectnode[user].begin(), nodeconnectnode[user].end(), item) == nodeconnectnode[user].end())
					nodeconnectnode[user].push_back(item);
			if (nodeconnectnode.find(item) == nodeconnectnode.end())
				nodeconnectnode[item].push_back(user);
			else
				if (std::find(nodeconnectnode[item].begin(), nodeconnectnode[item].end(), user) == nodeconnectnode[item].end())
					nodeconnectnode[item].push_back(user);
		}
	}
	fclose(fp);

	std::ofstream fmatch ("top10RecommendNoTimeBasedAlgriothm_p.txt",std::ios::out);
	fmatch << "p\thitration" << std::endl;
	for (float p = 0.1; p < 0.2; p += 0.1) {
		int total = 0;
		std::cout << "p is :" << p << std::endl;
		for (std::vector<std::string>::const_iterator i = userlist.begin(); i != userlist.end(); ++i) {
			total += 1;
			std::string user = *i;
			std::cout << "total user is :" << total << std::endl;

			//if (nodeconnectnode)
			std::string testdata = nodeconnectnode[user].back();
			std::cout << testdata << std::endl;

			//if (std::find(nodeconnectnode[user].begin(), nodeconnectnode[user].end(), testdata) == nodeconnectnode[user].end())
			//	std::cout << "False" << std::endl;
			std::multimap<float, std::string> recommend
				= mixPathAlgorithm(user, testdata, nodeconnectnode, nodeoutdegree,1, p);
		}
	}

	//for( std::map<std::string, int>::const_iterator i = nodeoutdegree.begin(); i != nodeoutdegree.end(); ++i)
    //	std::cout << i->first << "\t" << i->second << '\n';
//for (std::map<std::string, std::vector<std::string> >::iterator i = nodeconnectnode.begin(); i != nodeconnectnode.end(); ++i) {
//   std::cout << i->first << ": " << std::endl;
//   for (std::vector<std::string>::iterator j = i->second.begin(); j != i->second.end(); ++j) {
//      std::cout << *j << std::endl;
///   }
//}

	std::cout << "end" << "\n";
	return 1;

}