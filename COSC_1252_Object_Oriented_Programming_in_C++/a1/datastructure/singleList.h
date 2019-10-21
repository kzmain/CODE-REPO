#include <memory>
#include <string>
using namespace std;
class SingleList
{
    class Node
    {
        public:
			string word;
			Node* next;
		public:
		Node(string input):
			word(input),
			next(nullptr)
		{}
        //void set_next(std::unique_ptr<node>&& newnext);
        //node * get_next(void);
        //int get_data(void);
        //std::unique_ptr<node>& get_next_ptr(void);
        friend class linked_list;
    };
public:
    unique_ptr<Node> head;
	unique_ptr<Node> next;
	Node* current;
    int size;
public:
    SingleList():
		head(nullptr),
		current(nullptr),
		size(0) 
	{}
public:
	int add(string input){
		Node temp(input);
		if(head==nullptr){
			head = &temp;
			current = head;
			cout<<head->word<<"\n";
		}
		
	}
	int get(){
		current = head;
		//do{
			
			//current=next;
		//}while(next!=nullptr);
		
	}
    //bool add(int);
    //bool search(int);
};