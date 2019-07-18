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
 	//����������һ���ṹ�� �������˵��ò�����()
 	/*���÷�ʽ��
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
 	vector<vector<int> > dir = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};//�Թ����������߶�
	visited[start[0]][start[1]] = true;
	/*
	����Ҫ����ͷ�ļ�#include<queue>
	���壺priority_queue<Type, Container, Functional>
	Type:������������
	Container:�����������ͣ�Container������������ʵ�ֵ�������
	����vector,deque�ȵȣ��������� list��STL����Ĭ���õ���vector����
	Functional:���ǱȽϵķ�ʽ��
 	  ���ڻ������� Ĭ���Ǵ󶥶�(������ȳ�)
      priority_queue<int> a; 
 	  ��ͬ�� priority_queue<int, vector<int>, less<int> > a;
 	  ��������С���ѣ�С�����ȳ��� 
      priority_queue<int, vector<int>, greater<int> > c;  
	�Ͷ��л���������ͬ:

	top() 		���ʶ�ͷԪ��
	empty() 	�����Ƿ�Ϊ��
	size()  	���ض�����Ԫ�ظ���
	push() 		����Ԫ�ص���β (������)
	emplace() 	ԭ�ع���һ��Ԫ�ز��������
	pop() 		������ͷԪ��
	swap() 		��������
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