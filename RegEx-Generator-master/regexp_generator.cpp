#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm> 

using namespace std;

string generateRegExp_Recursive(const vector<string>& items, int charAt, int begin, int end){
	stringstream ss;

	bool optional(false);
	int nChar(0);

	int b = begin;
	while(b < end){
		if(items[b].size() <= charAt){
			++b;
			optional = true;
			continue;
		}

		const char c(items[b][charAt]);
		if(nChar > 0)
			ss << "|";
		ss << c;
		nChar++;

		int e(b+1);
		while(e < end && items[e][charAt] == c)
			e++;

		ss << generateRegExp_Recursive(items,charAt+1,b,e);
		b = e;
	}

	stringstream final_ss;
	if(nChar > 0){
		if(optional)
			final_ss << "(" << ss.str() << ")+";
		else{
			if(nChar == 1)
				return ss.str();
			final_ss << "(" << ss.str() << ")";
		}
	}

	return final_ss.str();
}

string generateRegExp(const vector<string>& items){
	return generateRegExp_Recursive(items, 0, 0, items.size());
}

int main(){
	ifstream file;
	file.open("ids.txt");
	string line;
	vector<string> items;

	while(getline(file, line))
		items.push_back(line);
	
	sort(items.begin(), items.end()); 

	cout << generateRegExp(items);
	return 0;
}
