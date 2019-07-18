#include <iostream>
#include <queue>
#include <vector>
#include <stack>
#include <cassert>
using namespace std;

typedef struct POINTS {
	int R;
	int C;
}Point;

class ShortestPath {
private:
	vector<vector <int>> &maze;
	int row = 0;
	int col = 0;
	int sum = 0;
	bool **visited;
	int **distance;
	Point **from;
	Point src, des;


public:
	bool isVal(int r, int c) {
		return((r >= 0 && r< row) && (c >= 0 && c < col));
	}
	bool pointIsVal(Point p) {
		return isVal(p.R, p.C);
	}
	bool isEual(Point src, Point des) {
		return ((src.R == des.R) && (src.C == des.C));
	}
	ShortestPath(vector<vector <int>> &maze_data, Point &s, Point &d) :maze(maze_data),src(s),des(d){
		assert(!maze.empty());
		int RowCal[] = { -1, 0, 0, 1 };
		int ColCal[] = { 0, -1, 1, 0 };

		row = maze.size();
		col = maze[0].size();
		sum = row * col;

		visited = new bool *[row];
		distance = new int *[row];
		from = new Point *[row];
		for (int i = 0; i < row; i++) {
			visited[i] = new bool[col];
			distance[i] = new int[col];
			from[i] = new Point[col];
		}

		for (int i = 0; i < row; i++)
			for (int j = 0; j < col; j++)
			{
				visited[i][j] = false;
				distance[i][j] = -1;
				from[i][j] = { -1,-1 };
			}

		queue<Point> q;
		visited[src.R][src.C] = true;
		distance[src.R][src.C] = 0;
		from[src.R][src.C] = { -1,-1 };
		q.push(src);
		while (!q.empty()) {
			Point cur = q.front();
			q.pop();
			if (isEual(cur, des))
				return;
			for (int i = 0; i < 4; i++) {
				int RowTemp = cur.R + RowCal[i];
				int ColTemp = cur.C + ColCal[i];
				if (isVal(RowTemp, ColTemp) && maze[RowTemp][ColTemp] && (!visited[RowTemp][ColTemp])) {
					visited[RowTemp][ColTemp] = true;
					distance[RowTemp][ColTemp] = distance[cur.R][cur.C] + 1;
					from[RowTemp][ColTemp] = { cur.R, cur.C };
					Point tmpPoint = { RowTemp ,ColTemp };
					q.push(tmpPoint);
				}
			}
		}
		cout << "Shortest Path doesn't exist" << endl;
	}

	~ShortestPath() {
		for (int i = 0; i < row; i++) {
			delete[] visited[i];
			delete[] distance[i];
			delete[] from[i];
		}
		delete[] visited;
		delete[] distance;
		delete[] from;
	}


	void GetPath(vector<Point> &vec, Point src, Point des) {
		stack<Point> s;
		Point tmp = des;
		vec.clear();
		if (!maze[src.R][src.C] || !maze[des.R][des.C]) {
			//return;
		}
		while (!isEual(tmp, src)) {
			s.push(tmp);
			tmp = from[tmp.R][tmp.C];
		}
		s.push(tmp);

		while (!s.empty()) {
			vec.push_back(s.top());
			s.pop();
		}
	}
	void ShowPath() {
		vector<Point> path;
		assert(pointIsVal(src) && pointIsVal(des));
		GetPath(path, src, des);
		cout << "the shortest distance:" << distance[des.R][des.C] << endl;
		for (int i = 0; i < path.size(); i++) {
			cout << "(" << path[i].R << "," << path[i].C << ")";
			if (i == path.size() - 1)
				cout << endl;
			else
				cout << " -> ";
		}
	}

};

int main() {
	vector<vector<int>> maze = {
		{ 1, 0, 1, 1, 1, 1, 0, 1, 1, 1 },
		{ 1, 0, 1, 0, 1, 1, 1, 0, 1, 1 },
		{ 1, 1, 1, 0, 1, 1, 0, 1, 0, 1 },
		{ 0, 0, 0, 0, 1, 0, 0, 0, 0, 1 },
		{ 1, 1, 1, 0, 1, 1, 1, 0, 1, 0 },
		{ 1, 0, 1, 1, 1, 1, 0, 1, 0, 0 },
		{ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1 },
		{ 1, 0, 1, 1, 1, 1, 0, 1, 1, 1 },
		{ 1, 1, 0, 0, 0, 0, 1, 0, 0, 1 }
	};
	Point src1 = { 0,0};
	Point des1 = { 3,4};
	Point src2 = { 0,0};
	Point des2 = { 8,9};
	cout << "The succeed case:" << endl;
	ShortestPath shortpath_succeed(maze, src1, des1);
	shortpath_succeed.ShowPath();

	cout << "The failed case:" << endl;
	ShortestPath shortpath_failed(maze, src2, des2);
	shortpath_failed.ShowPath();

	return 0;
}