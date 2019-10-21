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
#include "slist.h"
using namespace std;

int slist::add(string input)
{
    node* current = nullptr;
    node* prev = nullptr;
    unique_ptr<node> temp = make_unique<node>(input);
    //Header node
    if(head==nullptr){
        head = temp.release();
        ++size;
        return 0;
    }
    current = head;
    while(current!=nullptr){
        prev = current;
        current=current->next;
    }
    //Add node before head
    if(prev==nullptr)
    {

        head=temp.release();
        head->next = current;
        
    }
    //Add node at the end
    else if(current==nullptr){
        prev->next = temp.release();
    }
    //Add node at middle
    else
    {
        prev->next = temp.release();
        prev->next->next = current;
    }
    ++size;
    return 0;
}

string slist::get()
{
    string temp="";
    if(current==nullptr){
        current=head;
        temp = current->word;
        current = current->next;
    }
    else{
        temp = current->word;
        current = current->next;
    }
    return temp;
}


int slist::getSize(){
    return size;
}