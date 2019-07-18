#include <iostream>
#include <utility>
#include <unordered_map>
#include <vector>
#include<string>
#include<sstream>
using namespace std;

void build_unorderedMap(unordered_map<string,string> &um, vector<pair<string, string> > substitutes){
	for(auto sub : substitutes){
		um[sub.first] = sub.second;
	}
}

void getSubstitution(vector<vector<pair<int, string> > > vec_id_words, int depth, unordered_map<int, string>& curr, vector<unordered_map<int, string> >& res)
{
	if (curr.size() == vec_id_words.size()) {
		res.push_back(curr);
	}
	else {
		for (int i = 0; i < vec_id_words[depth].size(); ++i) {
			int id = vec_id_words[depth][0].first;
			string w = vec_id_words[depth][i].second;
			curr[id] = w;
			getSubstitution(vec_id_words, depth + 1, curr, res);curr.erase(id);
		}
	}
}

int main() {
	string sentence = " I am happy and sad";
	vector<pair<string, string>> substitutes = { {"happy", "glad"}, {"glad", "good"}, {"sad",
	"sorrow"} };
	// step 0. built our graph/map
	unordered_map<string, string> u_map;
	build_unorderedMap(u_map, substitutes);
	// step 1. split sentence into words
	vector<string> words;
	string word;
	istringstream iss(sentence);
	int id = -1;
	vector<vector<pair<int, string>>> vec_id_words;
	while (iss >> word) {
		++id;
		words.push_back(word);
		vector<pair<int, string>> id_words;
		// step 3. get to know if a word has a substitution
		if (u_map.find(word) == u_map.end()) {
			continue;
		}
		else {
			id_words.push_back({ id, word });
			while (u_map.find(word) != u_map.end()) {
				id_words.push_back({ id, u_map[word] });
				word = u_map[word];
			}
		}
		vec_id_words.push_back(id_words);
	}
	for (auto vec : vec_id_words) {
		for (auto id_word : vec) {
			cout << id_word.first << " " << id_word.second << endl;
		}
		cout << endl;
	}
	// step 4. get the cartesian product of these substitutions
	vector<unordered_map<int, string>> vec_id_string;
	unordered_map<int, string> curr;
	getSubstitution(vec_id_words, 0, curr, vec_id_string);
	for (auto umap : vec_id_string) {
		for (auto i : umap) {
			cout << i.first << " " << i.second << endl;
		}
		cout << endl;
	}
	// step 5. make sentence
	vector<string> sentences;
	for (int i = 0; i < vec_id_string.size(); ++i) {
		string sentence = "";
		id = -1;unordered_map<int, string> cur_ids_words = vec_id_string[i];
		for (int j = 0; j < words.size(); ++j) {
			++id;
			if (cur_ids_words.find(id) == cur_ids_words.end()) {
				sentence += words[j] + " ";
			}
			else {
				sentence += cur_ids_words[id] + " ";
			}
		}
		sentences.push_back(sentence);
	}
	for (auto s : sentences) {
		cout << s << endl;
	}
	char e;
	std::cin >> e;
	return 0;
}