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
class slist{
    public:
        class node{
            public:
                node* next;
                string word;
            public:
                node():next(nullptr),word(""){}
                node(string input):next(nullptr),word(input){}
                virtual ~node(){}
        };
    public:
        node* head;
        node* current=nullptr;
        int size=0;
        int i=0;
        slist(): head(nullptr),size(0){}
        virtual ~slist(){}
    public:
        int add(string input);
            
        string get();
        
        int getSize();
};



