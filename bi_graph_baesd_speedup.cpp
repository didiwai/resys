#include <iostream>
#include <vector>
#include <map>
#include <fstream>
#include <sstream>
#include <string>
#include <queue>
#include <algorithm>
#include <cmath>

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


std::multimap<float, int>
 mixPathAlgorithm(int user, std::map<int, std::vector<int> > &usernodeconnectnode, 
 std::map<int, std::vector<int> > &itemnodeconnectnode, 
 std::map<int, float> &userdegree, std::map<int, float> &itemdegree)
 {
	std::map<int, float> rank;
	rank[user] = 1;

	for (std::vector<int>::iterator i = usernodeconnectnode[user].begin(); i != usernodeconnectnode[user].end(); ++i)
	{
		float tempres_1 = 1 + userdegree[user];
		int item = *i;

		for (std::vector<int>::iterator j=itemnodeconnectnode[item].begin(); j != itemnodeconnectnode[item].end(); ++j)
		{
			int next_user = *j;
			if (next_user != user)
			{
				float tempres_2 = 1 + tempres_1 * itemdegree[item];

				for (std::vector<int>::iterator k = usernodeconnectnode[next_user].begin(); k != usernodeconnectnode[next_user].end(); ++k)
				{
					int last_item = *k;
					if (last_item != item) 
					{
						if (rank.find(last_item) == rank.end())
							rank[last_item] = 1 + tempres_2 * userdegree[next_user];
						else
							rank[last_item] = rank[last_item] + tempres_2 * userdegree[next_user];
					}
				}
			}	
		}
	}

	std::multimap<float, int> reverseTest = flip_map(rank);
	return reverseTest;
}


void createSimBetweenUserItem(std::map<int, float> &userdegree, std::map<int, float> &itemdegree, 
	std::map<int, int> *usernodeoutdegree, std::map<int, int> *itemnodeoutdegree, float p)
{
	int user, value;
	for( std::map<int, int>::const_iterator i = (*usernodeoutdegree).begin(); i != (*usernodeoutdegree).end(); ++i)
	{
		user = i->first;
		value = i->second;
		userdegree[user] = (1.0 / pow(value, p));
	}
	int item, itemvalue;
	for( std::map<int, int>::const_iterator j = (*itemnodeoutdegree).begin(); j != (*itemnodeoutdegree).end(); ++j)
	{
		item = j->first;
		itemvalue = j->second;
		itemdegree[item] = (1.0 / pow(itemvalue, p));
	}	

}

int main() {
	std::vector<int> userlist;
	std::map<int, int> usernodeoutdegree;
	std::map<int, int> itemnodeoutdegree;
	std::map<int, std::vector<int> > usernodeconnectnode;
	std::map<int, std::vector<int> > itemnodeconnectnode;
	std::map<int, int> testdata;

	FILE *fp = fopen("traindata.dat", "r");
	int user, item;

	while (fscanf(fp, "%d::%d", &user, &item) == 2) {

		if (std::find(userlist.begin(), userlist.end(), user) == userlist.end())
			userlist.push_back(user);
		//node degree
		if (usernodeoutdegree.find(user) == usernodeoutdegree.end())
			usernodeoutdegree[user] = 1;
		else
			usernodeoutdegree[user] = usernodeoutdegree[user] + 1;
		if (itemnodeoutdegree.find(item) == itemnodeoutdegree.end())
			itemnodeoutdegree[item] = 1;
		else
			itemnodeoutdegree[item] = itemnodeoutdegree[item] + 1;
		//node connect node
		if (usernodeconnectnode.find(user) == usernodeconnectnode.end())
			usernodeconnectnode[user].push_back(item);
		else
			if (std::find(usernodeconnectnode[user].begin(), usernodeconnectnode[user].end(), item) == usernodeconnectnode[user].end())
				usernodeconnectnode[user].push_back(item);
		
		if (itemnodeconnectnode.find(item) == itemnodeconnectnode.end())
			itemnodeconnectnode[item].push_back(user);
		else
			if (std::find(itemnodeconnectnode[item].begin(), itemnodeconnectnode[item].end(), user) == itemnodeconnectnode[item].end())
				itemnodeconnectnode[item].push_back(user);
	}
	fclose(fp);

	FILE *fpt = fopen("testdata.dat", "r");
	int usertest, itemtest;

	while (fscanf(fpt, "%d::%d", &usertest, &itemtest) == 2) {
		testdata[usertest] = itemtest;
	}
	fclose(fpt);

	std::ofstream fmatch ("top10RecommendNoTimeBasedAlgriothm_p.txt",std::ios::out);
	fmatch << "p\thitration" << std::endl;


	for (float p = 0.1; p < 0.2; p += 0.1) {
		int total = 0;
		std::map<int, float> userdegree;
		std::map<int, float> itemdegree;
		createSimBetweenUserItem(userdegree, itemdegree, &usernodeoutdegree, &itemnodeoutdegree, p);
		std::cout << "p is :" << p << std::endl;
		for (std::vector<int>::const_iterator i = userlist.begin(); i != userlist.end(); ++i) {
			total += 1;
			int user = *i;
			std::cout << "total user is :" << total << std::endl;

			//if (nodeconnectnode)
			std::multimap<float, int> recommend
				= mixPathAlgorithm(user, usernodeconnectnode, itemnodeconnectnode, userdegree, itemdegree);
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