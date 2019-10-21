/*****************************************************************\
*
*         Course code: COSC1252/1254
*         Student Number: s3560808
*         Date: 08.2017
*
*****************************************************************/
#include <memory>
#include <string>
#include <cstring>
using namespace std;

class bst{
    public:
        class node{
            public:
                node* left=nullptr;
                node* right=nullptr;
                node* parent=nullptr;
                string word;
                bool iterated = false;
            public:
                node():left(nullptr),right(nullptr),word(""){}
                node(string input):left(nullptr),right(nullptr),word(input){}
                virtual ~node(){}
        };
    public:
        int a = 0;
        node* head=nullptr;
        node* pivot=nullptr;
        int size;
    public:
        bst():head(nullptr),size(0){}
        virtual ~bst(){}
    public:
        int levenshtein(string str1,string str2);
        int add(string input);
        string get();
        node* get(node* pointer);
        void initialPivot();
        void initialPivot(node* initial);
};