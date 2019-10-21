#include <string.h>
#include <memory>
using namespace std;
class SingleList{
private:
	class Node{
	public:
		string data;
		unique_ptr<Node> leftNode;
		unique_ptr<Node> rightNode;
	public:
		Node()	
		{
			data = "";
			nextNode = nullptr;
		}
	public:
		int set(string inputWord, Node* next)
		{
			if(data==""){
				data = inputWord;
				nextNode.reset(next);
				return 1;
			}else{
				next->data=inputWord;
				return 0;
			}
			
		}
		string getdata(){
			return data;
		}
	};
public:
	Node firstNode;
	unique_ptr<Node> currentNode;
	int size=0;
public:
	SingleList(){
		
	}
public:
	void set(string inputWord){
		if(size==0)
		{
			currentNode.reset(&firstNode);
		}
		Node temp;
		int cir = currentNode->set(inputWord,&temp);
		if(cir==0){
			currentNode.reset(&temp);
		}
		++size;
		cout<<size<<"/n";
	}
};