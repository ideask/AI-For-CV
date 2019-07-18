#include <iostream>
#include <vector>
#include<queue>
using namespace std;
 struct Point{
 	int x;
 	int y;
 	int val;
 	Point(int r, int c, int v): x(r), y(c), val(r){}
 };
 
 struct QueueNode{
 	int dist;
 	Point p;
 	QueueNode(int d, Point point): dist(d), p(point){}
 };

 
 struct cmp{
 	//函数对象是一个结构体 它重载了调用操作符()
 	/*调用方式：
	 	struct cmp compare; 
	 	bool result = compare(a, b);
 	*/
 	bool operator()(QueueNode a, QueueNode b){
	 	return a.p.val > b.p.val;
	 }
 };
 
 int getShortestPath(vector<vector<int> > maze, vector<int> start, vector<int> end){
 	int rows = maze.size();
 	int cols = maze[0].size();
 	vector<vector<bool> >visited(rows, vector<bool>(cols, false));
 	vector<vector<int> > dir = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};//迷宫上下左右走动
	visited[start[0]][start[1]] = true;
	/*
	首先要包含头文件#include<queue>
	定义：priority_queue<Type, Container, Functional>
	Type:就是数据类型
	Container:就是容器类型（Container必须是用数组实现的容器，
	比如vector,deque等等，但不能用 list。STL里面默认用的是vector），
	Functional:就是比较的方式。
 	  对于基础类型 默认是大顶堆(大的数先出)
      priority_queue<int> a; 
 	  等同于 priority_queue<int, vector<int>, less<int> > a;
 	  这样就是小顶堆（小的数先出） 
      priority_queue<int, vector<int>, greater<int> > c;  
	和队列基本操作相同:

	top() 		访问队头元素
	empty() 	队列是否为空
	size()  	返回队列内元素个数
	push() 		插入元素到队尾 (并排序)
	emplace() 	原地构造一个元素并插入队列
	pop() 		弹出队头元素
	swap() 		交换内容
	*/
	priority_queue<QueueNode, vector<QueueNode>, cmp> pq;
	QueueNode s(0, Point(start[0], start[1], 0)); 
	pq.push(s);
	std::cout << "the path:" << std::endl;
	while(!pq.empty()){
		QueueNode cur = pq.top();
		if(cur.p.x == end[0] && cur.p.y == end[1]){
			return cur.dist;
		}
		pq.pop();

		int r = cur.p.x;
		int c = cur.p.y;
		for(int d = 0; d < 4; ++d){
			int nr = r + dir[d][0];
			int nc = c + dir[d][1];
			if(nr >= 0 && nr < rows && nc >= 0 && nc < cols && maze[nr][nc] && !visited[nr][nc] ){
				visited[nr][nc] = true;
				Point np(nr, nc, maze[nr][nc]);
				QueueNode newQueueNode(cur.dist + maze[nr][nc], np);
				pq.push(newQueueNode);
			}
		}

	}
	return -1;
 	
 	
 } 
 
 int main(){
 	vector<vector<int> > maze2 = {
	 	{1,1,1,1},
	    {2,1,0,1},
		{2,2,1,1},
	 };
	 vector<int> start = {0,0};
	 vector<int> end = {2,3};
	 int shortestPath;
	 shortestPath = getShortestPath(maze2, start, end);
	 std::cout << "shortest path length:" << shortestPath << std::endl;
	 char e;
	 std::cin >> e;
	 return 0;
	 
 }